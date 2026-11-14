"""TTG-17 background solver execution with a status endpoint."""
import asyncio
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request

from app.services.sample_data import demo_problem
from app.solver.engine import solve
from . import audit
from .schedule import replace_schedule
from .security import allow_generation, coordinator, current_user

router = APIRouter(prefix="/api", tags=["generation"])
_jobs = {}
_job_tasks = set()


def _solve_and_publish():
    result = solve(demo_problem())
    if result.status in ("OPTIMAL", "FEASIBLE"):
        replace_schedule(result.assignments)
    return {"status": result.status, "runtime_seconds": result.runtime_seconds,
            "soft_penalty": result.soft_penalty, "diagnostics": result.diagnostics}


@router.post("/generate", status_code=202)
async def generate(request: Request, user=Depends(coordinator)):
    allow_generation(request)
    job_id = uuid4().hex
    _jobs[job_id] = {"status": "queued"}

    async def worker():
        _jobs[job_id] = {"status": "running"}
        try:
            result = await asyncio.to_thread(_solve_and_publish)
            _jobs[job_id] = {"status": "complete", "result": result}
            audit.record(user["username"], "schedule.generate", result)
        except Exception as exc:
            _jobs[job_id] = {"status": "failed", "error": str(exc)}

    task = asyncio.create_task(worker())
    _job_tasks.add(task)
    task.add_done_callback(_job_tasks.discard)
    audit.record(user["username"], "schedule.generate.requested", {"job_id": job_id})
    return {"job_id": job_id, "status": "queued"}


@router.get("/jobs/{job_id}")
def get_job(job_id: str, user=Depends(current_user)):
    if job_id not in _jobs:
        raise HTTPException(404, detail="Generation job not found.")
    return {"job_id": job_id, **_jobs[job_id]}
