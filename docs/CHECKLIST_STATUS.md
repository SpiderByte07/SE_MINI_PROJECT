# Submission checklist status (v1.2)

This is a working evidence checklist for the current repo after TTG-14 to TTG-18 merged. It does not claim that an item is complete just because code or a document exists. Check the supplied course checklist and replace each `PENDING` only after attaching evidence.

| Checklist area | Current evidence/status | What remains before submission |
|---|---|---|
| SRS | Original SRS is in repo root; v1.1 addendum is in `docs/`. | Confirm it matches implemented behavior and attach the final revised copy if the instructor expects the updated requirements document itself. |
| SAD | Original SAD and v1.1 addendum are included. Web modules now exist under `backend/app/web/`. | Update architecture diagrams/component and sequence views to include the web UI/API, async generation, security and export; verify the addendum accurately reflects the merged design. |
| STP | v1.1 STP corrects the checklist's security-validation placement in section 5.1. `TEST_EXECUTION_MATRIX.md` maps current scope; this pack adds web integration tests. | Run the complete suite after all merges, refresh report and STP result totals; add remaining role/rate-limit/accessibility checks and review the generated evidence. |
| CI and tests | Main CI was observed running `pytest` with the original requirements. This pack adds `backend/tests/test_web_integration.py` and upgrades CI to install app/report dependencies, run the report script, and upload its output. | Run the suite locally and merge this change; confirm new CI succeeds. These new tests have not been run in this pack workspace. Do not use old green checks as evidence of new UI/security behavior. |
| Test reports | A generator and report instructions are included; no fresh report is bundled. | Run `python scripts/generate_reports.py` after applying this pack and commit actual `docs/reports/` outputs. Record real pass/fail/skip and coverage values; no hard-coded expected count. |
| User-facing demo | UI entry point is `backend/app/web/frontend/index.html`; run command is in README. | Start locally and capture a short screen recording showing login, filtered views, a valid/invalid move, exports and async generation. Save the actual recording under `docs/videos/` and verify it opens. |
| Jira / sprint evidence | Jira is the team's chosen tracker; TTG-14 to TTG-18 total 37 points and PRs #18-#21 are merged. | Ensure Jira shows accurate assignees, estimates, sprint dates/status and completed stories. Save screenshots/export if required by the course checklist. |
| PR review evidence | Merged work is in PRs #18-#21. | Keep PR pages with approvals and passing checks available. If the rubric requires a specific merger/reviewer role, report actual history as it is; do not rewrite or misstate it. |
| Contribution / repository metadata | Team and TTG ownership guidance is included. | Confirm each member's actual contribution/PR authors; complete GitHub About description/topics if your checklist asks for them. |
| Release / final package | No release tag or final freeze is asserted by this pack. | Create a release/tag only after final tests, docs, demo and checklist evidence are complete and the team agrees the repository is frozen. |

## Important implementation limits to disclose

- The demo schedule uses sample data. Do not present it as connected to a college's live timetable database.
- Async jobs and rate-limit buckets are process-memory state; jobs are not durable across restarts and multi-worker deployment needs shared state.
- SQLite audit events are local-file persistence. Resource data persistence is not equivalent to a production database.
- TLS is enforced only when configured behind a trusted HTTPS proxy. A local HTTP demo intentionally does not prove deployed TLS.
- The health endpoint is a point-in-time health signal; it cannot prove 99.5% uptime.
- Basic accessible markup and keyboard interactions do not prove formal WCAG 2.1 AA compliance. An accessibility audit is still needed.
- CI's existing solver tests do not by themselves verify the browser UI or all web/API paths.
