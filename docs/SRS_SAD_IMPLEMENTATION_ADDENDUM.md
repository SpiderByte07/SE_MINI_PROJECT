# SRS / SAD implementation addendum (v1.2)

This addendum updates the implementation view after TTG-14 through TTG-18. The original approved SRS and SAD PDFs remain in the repository root; use this addendum with them, and keep requirement identifiers stable for traceability.

## SRS status update

The current code includes a demo web UI, timetable views and filtering, schedule-move validation, PDF/XLSX export, asynchronous solver-job status, a health endpoint, an SQLite audit log, and login/role/security controls. The browser-facing application uses sample/demo timetable data. This implementation does not establish a live college deployment, institutional data integration, production uptime, or independently certified accessibility/security.

| Requirement area | Current implementation | Verification status |
|---|---|---|
| TT-F-012 | `/api/schedule` supports section/faculty/room views; UI exposes timetable filters. | Automated web tests are included in this pack; run them and attach UI evidence. |
| TT-F-013 | `/api/schedule/{entry_id}` validates moves and rejects conflicts. | Basic integration tests included; run and expand resource-conflict coverage. |
| TT-F-015 | `/api/export/pdf` and `/api/export/xlsx`. | Basic file-response tests included; run and open both generated files. |
| TT-NF-002 | `/api/health` reports a point-in-time status. | 99.5% uptime is not verified without a deployed measurement period. |
| TT-NF-003 | UI has accessibility-oriented controls. | Formal WCAG 2.1 AA conformance remains unverified pending an audit. |
| TT-NF-004 / TT-NF-005 | Async generation/status and audit operations are present. | In-process jobs/rate-limit state and local SQLite audit have documented limits; verify with test evidence. |
| TT-SR-001..005 | Login, token/role checks, HTTPS configuration, validation and rate limiting are present. | Use STP section 5.1 security test cases; do not claim external penetration testing. |

## SAD design update

The implementation is organized under `backend/app/web/`: `main.py` mounts routes and serves the UI; `schedule.py` provides timetable read/move operations; `generation.py` handles background solve jobs; `reports.py` produces PDF/XLSX; `security.py` applies login/token/role and request controls; `audit.py` stores audit events in SQLite; and `health.py` exposes a health signal. The solver remains under `backend/app/solver/` and sample input is supplied by `backend/app/services/sample_data.py`.

The UI/API integration is demonstrator scope: schedule and job data is process-local, async work is not durable across restarts, and deployment-level TLS requires a trusted proxy. Update the approved SAD diagram/sequence views if the course requires diagrams to show these added modules; do not present the prose here as a replacement for a required diagram.
