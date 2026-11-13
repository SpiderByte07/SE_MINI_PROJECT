"""Schedule view, clash-safe drag/drop, and asynchronous solver job endpoints."""
from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.services.sample_data import demo_problem
from app.solver.engine import solve
from . import audit
from .security import coordinator, current_user

router = APIRouter(prefix="/api", tags=["timetable"])
_entries = None


def _ensure_schedule():
    global _entries
    if _entries is None:
        result = solve(demo_problem())
        if result.status not in ("OPTIMAL", "FEASIBLE"):
            raise HTTPException(503, detail="The demo schedule could not be generated.")
        _entries = [asdict(item) | {"id": i + 1} for i, item in enumerate(result.assignments)]
    return _entries


def replace_schedule(assignments):
    global _entries
    _entries = [asdict(item) | {"id": i + 1} for i, item in enumerate(assignments)]


class MoveRequest(BaseModel):
    day: int = Field(ge=0, le=4)
    period: int = Field(ge=0, le=5)


def _overlap(existing, day, period, moving_length):
    return existing["day"] == day and max(existing["period"], period) < min(
        existing["period"] + existing["length"], period + moving_length)


def _conflict(candidate, day, period, entries):
    if period + candidate["length"] > 6:
        return "A class block cannot extend past the last period."
    for other in entries:
        if other["id"] == candidate["id"] or not _overlap(other, day, period, candidate["length"]):
            continue
        if other["section_id"] == candidate["section_id"]:
            return f"Section {candidate['section_id']} already has {other['course_code']} in that time."
        if other["faculty_id"] == candidate["faculty_id"]:
            return f"Faculty {candidate['faculty_id']} already teaches {other['course_code']} in that time."
        if other["room_id"] == candidate["room_id"]:
            return f"Room {candidate['room_id']} is already in use in that time."
    return None


@router.get("/schedule")
def get_schedule(view: str = "section", value: str | None = None, user=Depends(current_user)):
    if view not in {"section", "faculty", "room"}:
        raise HTTPException(422, detail="view must be section, faculty or room.")
    key = {"section": "section_id", "faculty": "faculty_id", "room": "room_id"}[view]
    if value == "":
        value = None
    entries = _ensure_schedule()
    selected = [e for e in entries if value is None or e[key] == value]
    return {"view": view, "value": value, "days": 5, "periods": 6, "assignments": selected}


@router.put("/schedule/{entry_id}")
def move_class(entry_id: int, move: MoveRequest, user=Depends(coordinator)):
    entries = _ensure_schedule()
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if entry is None:
        raise HTTPException(404, detail="Class assignment not found.")
    problem = _conflict(entry, move.day, move.period, entries)
    if problem:
        raise HTTPException(409, detail=problem)
    old = {"day": entry["day"], "period": entry["period"]}
    entry.update(day=move.day, period=move.period)
    audit.record(user["username"], "schedule.move", {"entry_id": entry_id, "from": old,
                                                       "to": {"day": move.day, "period": move.period}})
    return entry


