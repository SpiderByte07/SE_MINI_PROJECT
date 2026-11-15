 # STP-to-implementation verification matrix (v1.3)

This matrix reflects the local test run on 15 Nov 2026 using Windows and Python 3.11.9: **59 tests passed, 0 failed, 0 skipped; backend app line coverage was 90.7%**. One Starlette deprecation warning appeared but did not fail the run. See `docs/reports/summary.md`.

| Test area / STP reference | Requirement/story | Current implementation | Evidence / status |
|---|---|---|---|
| Core solver and resource cases | TT-F-001 to TT-F-011, TT-F-014 | Solver/unit suite | Passed as part of the 59-test run. See `docs/reports/summary.md`. |
| Multi-view timetable | TT-F-012 / TTG-14 | `/api/schedule` views and UI filters | Basic filter and invalid-view tests passed. Manual browser demo remains pending. |
| Move validation | TT-F-013 / TTG-15 | `PUT /api/schedule/{entry_id}` | Valid move, section conflict, invalid bounds, and unknown-ID tests passed. Faculty/room conflict evidence remains pending. |
| PDF / Excel output | TT-F-015 / TTG-16 | `/api/export/pdf`, `/api/export/xlsx` | Basic response and file-signature tests passed. Manually open both files and verify filtered exports before marking complete. |
| Async generation / health | TT-NF-004 and related operations / TTG-17 | `/api/generate`, `/api/jobs/{job_id}`, `/api/health` | Job acceptance, polling, and missing-job tests passed. A positive health endpoint check remains pending. Job state is in memory. |
| Audit log | TT-NF-005 / TTG-17 | SQLite audit module and `/api/audit` | Audit after a move passed. Generation-event and role-denial checks remain pending. |
| Security | TT-SR-001..005 / TTG-18 | Login, JWT, roles, input validation, optional HTTPS enforcement, and process-local rate limits | Basic login failure, unauthenticated access, input validation, and HTTPS tests passed. Role and rate-limit checks remain pending. No external security audit is claimed. |
| Accessibility | TT-NF-003 / TTG-17 | UI labels and keyboard support | Manual keyboard and screen-reader checks, plus a WCAG audit, remain pending. Do not claim AA conformance until verified. |
| Availability | TT-NF-002 | Health endpoint | Deployment and uptime monitoring remain pending. The health endpoint alone does not prove availability or 99.5% uptime. |

## Reports and reruns

The current reports are in `docs/reports/`, including `summary.md`, `junit.xml`, `test-report.html`, and coverage output. Keep these results with the revision they tested.

To rerun after code changes, from the repository root:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/generate_reports.py
