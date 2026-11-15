# STP-to-implementation verification matrix (v1.2)

This matrix records what needs to be demonstrated on the merged revision. The pack adds `backend/tests/test_web_integration.py` for basic UI/API smoke, view filtering, move validation, exports, async job polling, login and HTTPS behavior. Those tests are still pending execution. Mark a row PASS only after the fresh report or reproducible manual evidence confirms it.

| Test area / STP reference | Requirement/story | Current implementation | Evidence to attach / status |
|---|---|---|---|
| Core solver and resource cases | TT-F-001 to TT-F-011, TT-F-014 | Solver/unit suite | Existing pytest suite; record latest run in generated report. |
| Multi-view timetable | TT-F-012 / TTG-14 | `/api/schedule` views and UI filters | Basic filter/invalid-view tests included; PENDING fresh run and manual UI demo. |
| Move validation | TT-F-013 / TTG-15 | `PUT /api/schedule/{entry_id}` | Basic valid move, section conflict, bounds and unknown-ID tests included; PENDING fresh run and faculty/room conflict evidence. |
| PDF / Excel output | TT-F-015 / TTG-16 | `/api/export/pdf`, `/api/export/xlsx` | Basic response/file-signature tests included; PENDING fresh run and opening files / confirming filter. |
| Async generation / health | TT-NF-004 and related ops / TTG-17 | `/api/generate`, `/api/jobs/{job_id}`, `/api/health` | Job accept/poll/missing-ID test included; PENDING fresh run and health endpoint test. In-memory job limitation documented. |
| Audit log | TT-NF-005 / TTG-17 | SQLite audit module and `/api/audit` | Audit after move test included; PENDING fresh run, generation event and role-denial checks. |
| Security | TT-SR-001..005 / TTG-18 | Login, JWT, roles, input validation, optional HTTPS enforcement and process-local rate limits | Basic login failure, unauthenticated access, validation and HTTPS tests included; PENDING fresh run, role/rate-limit tests. No external security audit claimed. |
| Accessibility | TT-NF-003 / TTG-17 | UI labels/keyboard support | PENDING: manual keyboard and screen-reader checks plus WCAG audit; do not claim AA conformance until verified. |
| Availability | TT-NF-002 | Health endpoint | PENDING: deployment and uptime monitoring period; health endpoint alone is not availability evidence. |

## Fresh run procedure

From the repository root, after merging this pack:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/generate_reports.py
```

Commit the real output under `docs/reports/`. Update this matrix and the STP with actual case IDs and results. Never put expected totals or guessed coverage values in the report.
