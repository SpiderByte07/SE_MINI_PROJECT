"""TTG-17 liveness/readiness endpoint; production uptime must be monitored externally."""
from datetime import datetime, timezone

from fastapi import APIRouter
from . import audit

router = APIRouter(prefix="/api", tags=["operations"])
STARTED_AT = datetime.now(timezone.utc)


@router.get("/health")
def health():
    try:
        audit.recent(1)
        storage = "ok"
    except Exception:
        storage = "error"
    return {"status": "ok" if storage == "ok" else "degraded", "started_at": STARTED_AT,
            "checked_at": datetime.now(timezone.utc), "audit_storage": storage}
