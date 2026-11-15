# College Timetable Generation System

The project generates college timetables with an OR-Tools CP-SAT solver. The merged TTG-14 to TTG-18 work adds a filterable timetable UI, validated schedule moves, PDF/Excel export, asynchronous generation and job status, health/audit endpoints, and login/role/security controls.

## Run locally (Windows)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
$env:TTG_JWT_SECRET = 'replace-with-a-random-secret-at-least-32-characters'
$env:TTG_DEMO_USER = 'coordinator'
$env:TTG_DEMO_PASSWORD = 'replace-with-a-password-at-least-12-characters'
uvicorn app.web.main:app --app-dir backend --reload
```

Open `http://127.0.0.1:8000/` for the UI and `http://127.0.0.1:8000/api/docs` for API docs. Use demo credentials and sample data only.

Run tests from the repository root with `python -m pytest`. Generate reports with `python scripts/generate_reports.py`.

## Documents and evidence

- [Submission checklist status](docs/CHECKLIST_STATUS.md)
- [Web architecture supplement and sequence diagrams](docs/architecture/WEB_ARCHITECTURE.md)
- [STP-to-implementation matrix](docs/TEST_EXECUTION_MATRIX.md)
- [STP security validation section](docs/STP_SECTION_5.1_SECURITY_VALIDATION.md)
- [STP v1.2 test-results addendum](docs/STP_Test_Results_v1.2.pdf)
- [Latest generated test summary](docs/reports/summary.md)
- [Demo recording outline](docs/DEMO_VIDEO_SCRIPTS.md)

The STP v1.2 addendum supersedes the earlier fixed test totals with the latest observed run: 59 passed, 0 failed, 0 skipped, and 90.7% backend app line coverage. Read it together with the STP v1.1 document, which contains the security-validation section 5.1. Do not claim accessibility conformance, production security certification, or deployment uptime without separate evidence.

## Merged UI stories

TTG-14 (8 points), TTG-15 (8), TTG-16 (5), TTG-17 (8), and TTG-18 (8) are merged in PRs #18-#21, for 37 points total. Jira is the team's sprint tracker; see Jira for actual assignees and status.
