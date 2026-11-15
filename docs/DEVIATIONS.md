# Implementation notes and deviations (v1.2)

This document summarizes the current repository after TTG-14 to TTG-18 were merged. The original SRS/SAD/STP describe the target system; see `CHECKLIST_STATUS.md` for evidence still required before submission.

## Delivered scope

The repository contains the OR-Tools timetable solver plus a demo web layer under `backend/app/web/`: timetable views, move validation, PDF/Excel export, asynchronous generation/job status, health and audit endpoints, and login/role/security controls. The UI and API use sample timetable data. TTG-14 to TTG-18 have merged PRs #18-#21, estimated at 37 points total.

## Limits and deviations to disclose

| Area | Current behavior / limit |
|---|---|
| Data | Schedule data is generated from demo data and held in process memory. SQLite stores audit events; this is not a persistent institutional resource database. |
| Async generation | Work is run in a background task/thread in the same application process. Job state is in memory and is lost on restart; this is not a durable distributed job queue. |
| Security | Login, role checks, password hashing, request validation and in-process rate limits are implemented. Configure strong `TTG_JWT_SECRET` and demo credentials. TLS enforcement depends on deployment behind a trusted TLS proxy. Do not claim a production security audit. |
| Reliability | `/api/health` reports a current health status. It does not establish 99.5% service uptime; that requires a deployed service and measurement over the required period. |
| Accessibility | UI includes accessibility-oriented labels/keyboard behavior, but no independent WCAG 2.1 AA audit is included. State this as work implemented, conformance pending audit. |
| Verification | The existing CI check runs the repository's pytest suite. Prior green runs predate this documentation/CI update and must not be represented as proof of browser-level integration coverage. Generate fresh test results after merging. |
| Process | Sprint planning/story points are tracked in Jira, accepted by the team in place of a GitHub Project. Preserve actual Jira and pull-request records. |

## Final reporting rule

Keep statements about tests, coverage, accessibility, security, uptime, and release status tied to fresh, reproducible evidence. Do not copy the old fixed test totals or coverage estimate from v1.1 documents into the final report; use the fresh generated report and update the STP accordingly.
