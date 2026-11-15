# Submission checklist status (v1.4)

This checklist reflects the merged TTG-14 to TTG-18 implementation and the latest local automated test run. Mark an item complete only when its evidence is included and checked.

## Latest automated test run

- Date: 15 Nov 2026
- Environment: Windows, Python 3.11.9
- Tests: **59 passed, 0 failed, 0 skipped**
- Backend app line coverage: **90.7%**
- Result: **PASS**
- One Starlette deprecation warning appeared; it did not fail the run.
- Report: `docs/reports/summary.md`
- STP figures: `docs/STP_Test_Results_v1.2.pdf` supersedes the earlier v1.1 test totals.

| Checklist area | Current evidence/status | What remains before submission |
|---|---|---|
| SRS | Original SRS and v1.1 addendum are in the repository. | Confirm the requirements match the implemented demo. Attach a final revised SRS if the instructor requires the revised document itself. |
| SAD | Original SAD and v1.1 addendum are included. Web architecture diagrams and sequences are in `docs/architecture/WEB_ARCHITECTURE.md`. | Confirm the supplement satisfies the course format; incorporate it into the SAD PDF if required. |
| STP | STP v1.1 has security validation in section 5.1. The v1.2 results addendum records 59 passed, 0 failed, 0 skipped, and 90.7% coverage. | Keep both documents together. Complete the manual/extended cases below and update the STP again if a later run changes the results. |
| CI and tests | Fresh local run passed 59/59 tests. The integration tests cover basic web/API behavior. | Confirm the GitHub Actions check is green for the final documentation PR. |
| Test reports | Fresh reports are in `docs/reports/`, including summary, JUnit, HTML, and coverage outputs. | Ensure the reports correspond to the final code revision and remain committed. |
| User-facing demo | UI entry point is `backend/app/web/frontend/index.html`; run instructions are in README. | Record a short demo showing login, filters, valid/invalid moves, exports, and async generation. Add the actual recording under `docs/videos/` and verify playback. |
| Jira / sprint evidence | Jira tracks the work; TTG-14 to TTG-18 total 37 points. | Confirm assignees, estimates, sprint dates/status, and completion. Save screenshots/export if required by the course checklist. |
| PR review evidence | TTG-14 to TTG-18 code was merged in PRs #18-#21; final documentation changes are tracked through a PR. | Keep approval and passing-check evidence available; accurately report actual reviewers/mergers. |
| Contribution / repository metadata | Team and TTG ownership guidance is included. | Confirm actual member contributions and fill GitHub About description/topics if required. |
| Release / final package | No release tag or final freeze is claimed. | Tag/release only after required evidence and documentation are complete. |

## Manual and deployment checks still pending

- Accessibility: perform keyboard and screen-reader checks; do not claim WCAG 2.1 AA without an audit.
- Security: run the remaining role and rate-limit cases; no external security audit is claimed.
- Exports: manually open the generated PDF and Excel files and verify filtered exports.
- Availability: health is a point-in-time signal; it does not prove 99.5% uptime. A deployment and monitoring period are required.
- Demo: the schedule uses sample data and is not connected to a college's live timetable database.

## Implementation limits to disclose

- Schedule data and asynchronous job state are held in process memory and do not survive restarts.
- SQLite stores local audit events; resource data persistence is not equivalent to a production institutional database.
- TLS enforcement requires deployment behind a trusted HTTPS proxy.
