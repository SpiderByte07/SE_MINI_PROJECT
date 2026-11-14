"""FastAPI integration entry point. Run with: uvicorn app.web.main:app --app-dir backend"""
import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import audit
from .reports import router as reports_router
from .schedule import router as schedule_router
from .generation import router as generation_router
from .health import router as health_router
from .security import allow_login, enforce_https, issue_token, authenticate_user, current_user

app = FastAPI(title="College Timetable API", version="1.1", docs_url="/api/docs")
app.include_router(schedule_router)
app.include_router(reports_router)
app.include_router(generation_router)
app.include_router(health_router)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=1, max_length=128)


@app.middleware("http")
async def security_headers_and_transport(request: Request, call_next):
    try:
        enforce_https(request)
    except HTTPException as exc:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
    return response


@app.post("/api/login")
def login(payload: LoginRequest, request: Request):
    allow_login(request)
    role = authenticate_user(payload.username, payload.password)
    if role is None:
        raise HTTPException(401, detail="Invalid username or password.")
    token = issue_token(payload.username, role)
    audit.record(payload.username, "auth.login", {"role": role})
    return {"access_token": token, "token_type": "bearer", "expires_in_minutes": 45}


@app.get("/api/audit")
def audit_events(limit: int = 50, user=Depends(current_user)):
    if user["role"] != "coordinator":
        raise HTTPException(403, detail="Coordinator role required.")
    return {"events": audit.recent(limit)}


@app.get("/", include_in_schema=False)
def ui():
    return FileResponse(os.path.join(os.path.dirname(__file__), "frontend", "index.html"))
