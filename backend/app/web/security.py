"""Authentication, roles, HTTPS policy and small in-memory rate limiter."""
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from functools import lru_cache
import json
import os
import time

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
TOKEN_MINUTES = 45
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)
_login_failures = defaultdict(deque)
_generation_calls = defaultdict(deque)


def _secret():
    secret = os.getenv("TTG_JWT_SECRET", "")
    if len(secret) < 32:
        raise RuntimeError("Set TTG_JWT_SECRET to a random value of at least 32 characters.")
    return secret


def issue_token(username: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": username, "role": role, "iat": now,
                       "exp": now + timedelta(minutes=TOKEN_MINUTES)}, _secret(), algorithm=ALGORITHM)


def verify_demo_password(password: str) -> bool:
    """Backward-compatible helper for the coordinator demo account."""
    return authenticate_user(os.getenv("TTG_DEMO_USER", "coordinator"), password) == "coordinator"


@lru_cache(maxsize=64)
def _password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    """Read demo accounts from JSON env config; bcrypt-hash configured values in memory."""
    raw_accounts = os.getenv("TTG_ACCOUNTS_JSON", "")
    if raw_accounts:
        try:
            accounts = json.loads(raw_accounts)
        except json.JSONDecodeError:
            raise RuntimeError("TTG_ACCOUNTS_JSON must be valid JSON.") from None
        account = accounts.get(username)
        if not isinstance(account, dict) or account.get("role") not in {"coordinator", "faculty", "student"}:
            return None
        password_value = str(account.get("password", ""))
        role = account["role"]
    else:
        if username != os.getenv("TTG_DEMO_USER", "coordinator"):
            return None
        password_value = os.getenv("TTG_DEMO_PASSWORD", "")
        role = "coordinator"
    if len(password_value) < 12:
        raise RuntimeError("Configured demo passwords must be at least 12 characters.")
    return role if pwd_context.verify(password, _password_hash(password_value)) else None


async def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in required.",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(credentials.credentials, _secret(), algorithms=[ALGORITHM])
        return {"username": payload["sub"], "role": payload["role"]}
    except (JWTError, KeyError, RuntimeError):
        raise HTTPException(status_code=401, detail="Token is invalid or expired.",
                            headers={"WWW-Authenticate": "Bearer"}) from None


def coordinator(user=Depends(current_user)):
    if user["role"] != "coordinator":
        raise HTTPException(status_code=403, detail="Coordinator role required.")
    return user


def enforce_https(request: Request):
    """Enable behind a trusted TLS proxy with TTG_REQUIRE_HTTPS=1."""
    if os.getenv("TTG_REQUIRE_HTTPS") == "1":
        forwarded = request.headers.get("x-forwarded-proto", "").lower()
        if request.url.scheme != "https" and forwarded != "https":
            raise HTTPException(status_code=426, detail="HTTPS is required.")


def allow_login(request: Request):
    return _allow(request.client.host if request.client else "unknown", _login_failures, 10, 60)


def allow_generation(request: Request):
    return _allow(request.client.host if request.client else "unknown", _generation_calls, 5, 60)


def _allow(key, buckets, limit, seconds):
    now = time.monotonic()
    bucket = buckets[key]
    while bucket and now - bucket[0] >= seconds:
        bucket.popleft()
    if len(bucket) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    bucket.append(now)
