# Submission checklist status (v1.3)

This checklist reflects the repository after TTG-14 to TTG-18 merged and the latest local automated test run. Mark an item complete only when its evidence is included and checked.

## Latest automated test run

- Date: 15 Nov 2026
- Environment: Windows, Python 3.11.9
- Tests: **59 passed, 0 failed, 0 skipped**
- Backend app line coverage: **90.7%**
- Result: **PASS**
- One Starlette deprecation warning appeared; it did not cause a test failure.
- Report: `docs/reports/summary.md`

| Checklist area | Current evidence/status | What remains before submission |
|---|---|---|
| SRS | Original SRS is in the repo root; v1.1 addendum is in `docs/`. | Confirm the requirements match the implemented behavior. Include a final revised copy if the instructor expects the updated SRS itself. |
| SAD | Original SAD and v1.1 addendum are included. Web modules exist under `backend/app/web/`. | Update the architecture diagrams and sequence views to show the UI/API, async generation, security, and export. |
| STP | The v1.1 STP corrects the placement of security validation in section 5.1. The latest local suite passed 59/59 tests with 90.7% coverage. | Update the STP’s old test totals and coverage figures to match this run. Add results for remaining role, rate-limit, accessibility, and manual checks. |
| CI and tests | Web integration tests are included. The latest local test run passed: 59 passed, 0 failed, 0 skipped. | Confirm CI passes for the updated branch or PR. The automated tests do not replace a full browser demo or a formal accessibility/security audit. |
| Test reports | Fresh reports are present under `docs/reports/`, including `summary.md`, JUnit, HTML, and coverage files. | Confirm the reports are committed and correspond to the final merged code. |
| User-facing demo | UI entry point: `backend/app/web/frontend/index.html`. The README has local run instructions. | Record a short demo showing login, filters, valid/invalid moves, exports, and async generation. Save the actual video under `docs/videos/` and check playback. |
| Jira / sprint evidence | Jira tracks the team’s work. TTG-14 to TTG-18 total 37 points; PRs #18-#21 are merged. | Confirm Jira shows the correct assignees, estimates, sprint dates/status, and completed stories. Save screenshots or an export if the course requires them. |
| PR review evidence | Merged work is in PRs #18-#21. | Keep the PRs’ approvals and passing checks available. Report the actual review/merge history accurately. |
| Contribution / repository metadata | Team and TTG ownership guidance is included. | Confirm member contributions and PR authors. Fill in the GitHub About description/topics if required by the checklist. |
| Release / final package | No release tag or final freeze is claimed. | Create a release/tag only after final tests, documents, demo, and checklist evidence are complete. |

## Implementation limits to disclose

- The timetable uses sample data; it is not connected to a college’s live timetable database.
- Async jobs and rate-limit counters are held in process memory. Jobs do not survive restarts, and multi-worker deployment needs shared state.
- SQLite stores audit events locally; this is not a persistent institutional resource database.
- TLS enforcement depends on configuring the app behind a trusted HTTPS proxy.
- The health endpoint reports current health; it does not prove 99.5% uptime.
- Accessibility-oriented controls do not prove WCAG 2.1 AA conformance. A formal audit is still needed.
- The integration tests cover basic web/API behavior, but manual UI checks and additional role/rate-limit checks remain.
