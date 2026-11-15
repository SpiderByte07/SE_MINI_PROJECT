# College Timetable Generation System

The project generates conflict-free college timetables with an OR-Tools CP-SAT solver. The merged TTG-14 to TTG-18 work adds a filterable timetable UI, validated schedule moves, PDF/Excel export, asynchronous generation and status, health/audit endpoints, and login/role/security controls.

## Team

| Name | SRN |
|---|---|
| Saathvik Sai Suvarna | PES1UG24AM238 |
| Ayush PM | PES1UG24AM909 |
| Rishi Bharadwaj | PES1UG24AM223 |
| Rohit Chaki | PES1UG24AM228 |

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

Open `http://127.0.0.1:8000/` for the UI and `http://127.0.0.1:8000/api/docs` for API docs. Sign in with the demo user/password configured above. Use only local/demo data; production deployment and security hardening are not established by this project.

Run the existing automated suite from the repo root with `python -m pytest`. Run `python scripts/generate_reports.py` to create test reports after the script and developer dependencies from this pack are installed.

## Project evidence

- [Checklist status and remaining submission work](docs/CHECKLIST_STATUS.md)
- [Implementation deviations and limits](docs/DEVIATIONS.md)
- [STP test execution matrix](docs/TEST_EXECUTION_MATRIX.md)
- [Demo recording outline](docs/DEMO_VIDEO_SCRIPTS.md)
- [Phase 1 documents](SRS_College_Timetable_Generation_System.pdf, SAD_College_Timetable_Generation_System.pdf, STP_College_Timetable_Generation_System.pdf)

The original SRS/SAD/STP remain in the repository root. The v1.1 addenda in `docs/` update earlier documentation; read them with `docs/SRS_SAD_IMPLEMENTATION_ADDENDUM.md` and this v1.2 implementation status. The STP v1.1 corrected the placement of security validation in section 5.1, but its old fixed test totals are historical. Use fresh results from `docs/reports/summary.md` and update the STP before final submission.

## Merged UI stories

TTG-14 (8 points), TTG-15 (8), TTG-16 (5), TTG-17 (8) and TTG-18 (8) are merged in PRs #18-#21 (37 points total). See Jira for individual ownership and sprint status. A merged PR is not evidence that every feature has been independently integration-tested; complete the remaining items in `docs/CHECKLIST_STATUS.md` before submission.
