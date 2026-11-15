"""Integration checks for the merged TTG-14 to TTG-18 web/API layer."""
import time

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def web_client(monkeypatch, tmp_path):
    monkeypatch.setenv("TTG_JWT_SECRET", "test-secret-key-at-least-32-characters-long")
    monkeypatch.setenv("TTG_DEMO_USER", "coordinator")
    monkeypatch.setenv("TTG_DEMO_PASSWORD", "demo-password-long-enough")
    monkeypatch.delenv("TTG_ACCOUNTS_JSON", raising=False)
    monkeypatch.delenv("TTG_REQUIRE_HTTPS", raising=False)

    from app.web import audit, generation, schedule
    from app.web.main import app
    from app.web.security import _password_hash

    monkeypatch.setattr(audit, "DB_PATH", tmp_path / "audit.sqlite3")
    monkeypatch.setattr(schedule, "_entries", [
        {"id": 1, "day": 0, "period": 0, "length": 1, "course_code": "CS101",
         "section_id": "S1", "faculty_id": "F1", "room_id": "R1"},
        {"id": 2, "day": 0, "period": 1, "length": 1, "course_code": "MA101",
         "section_id": "S2", "faculty_id": "F2", "room_id": "R2"},
    ])
    generation._jobs.clear()
    _password_hash.cache_clear()
    with TestClient(app) as client:
        yield client
    _password_hash.cache_clear()


def token(client):
    response = client.post("/api/login", json={
        "username": "coordinator", "password": "demo-password-long-enough",
    })
    assert response.status_code == 200
    return response.json()["access_token"]


def auth(token_value):
    return {"Authorization": f"Bearer {token_value}"}


def test_ui_is_served_with_security_headers(web_client):
    response = web_client.get("/")
    assert response.status_code == 200
    assert "College Timetable" in response.text
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_schedule_requires_login(web_client):
    response = web_client.get("/api/schedule")
    assert response.status_code == 401


def test_schedule_views_filter_and_reject_bad_view(web_client):
    headers = auth(token(web_client))
    filtered = web_client.get("/api/schedule?view=faculty&value=F1", headers=headers)
    assert filtered.status_code == 200
    assert [row["id"] for row in filtered.json()["assignments"]] == [1]
    assert web_client.get("/api/schedule?view=bad", headers=headers).status_code == 422


def test_drag_move_succeeds_and_records_audit_event(web_client):
    headers = auth(token(web_client))
    response = web_client.put("/api/schedule/1", headers=headers, json={"day": 1, "period": 2})
    assert response.status_code == 200
    events = web_client.get("/api/audit", headers=headers).json()["events"]
    assert any(event["action"] == "schedule.move" for event in events)


def test_drag_move_rejects_conflict_and_out_of_range(web_client):
    from app.web.schedule import _entries
    _entries[1]["section_id"] = "S1"
    headers = auth(token(web_client))
    conflict = web_client.put("/api/schedule/1", headers=headers, json={"day": 0, "period": 1})
    assert conflict.status_code == 409
    invalid = web_client.put("/api/schedule/1", headers=headers, json={"day": 5, "period": 0})
    assert invalid.status_code == 422
    assert web_client.put("/api/schedule/999", headers=headers, json={"day": 1, "period": 1}).status_code == 404


def test_pdf_and_excel_exports_return_expected_files(web_client):
    headers = auth(token(web_client))
    pdf = web_client.get("/api/export/pdf?view=section&value=S1", headers=headers)
    xlsx = web_client.get("/api/export/xlsx?view=section&value=S1", headers=headers)
    assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")
    assert xlsx.status_code == 200 and xlsx.content.startswith(b"PK")


def test_generation_job_can_be_polled(web_client, monkeypatch):
    from app.web import generation
    monkeypatch.setattr(generation, "_solve_and_publish", lambda: {
        "status": "OPTIMAL", "runtime_seconds": 0.01, "soft_penalty": 0, "diagnostics": [],
    })
    headers = auth(token(web_client))
    started = web_client.post("/api/generate", headers=headers)
    assert started.status_code == 202
    job_id = started.json()["job_id"]
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        status = web_client.get(f"/api/jobs/{job_id}", headers=headers)
        assert status.status_code == 200
        if status.json().get("status") in {"complete", "failed"}:
            break
        time.sleep(0.01)
    assert status.json()["status"] == "complete"
    assert web_client.get("/api/jobs/not-a-job", headers=headers).status_code == 404


def test_login_rejects_bad_credentials(web_client):
    response = web_client.post("/api/login", json={
        "username": "coordinator", "password": "incorrect-password",
    })
    assert response.status_code == 401


def test_https_can_be_required_by_configuration(web_client, monkeypatch):
    monkeypatch.setenv("TTG_REQUIRE_HTTPS", "1")
    response = web_client.get("/api/health")
    assert response.status_code == 426
