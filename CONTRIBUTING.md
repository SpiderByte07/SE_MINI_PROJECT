# Contributing and project tracking

## Team workflow

Use the shared GitHub repository, feature branches, pull requests, a teammate review, and a passing CI check. Do not push directly to protected `main`. Track stories, owners, estimates, and sprint progress in Jira (the team's accepted project tracker).

1. `git checkout main` and `git pull` before starting.
2. Create one branch per change and include relevant automated tests.
3. Run `python -m pytest` locally.
4. Open a PR linked to the Jira story. Request a teammate review and wait for CI.
5. Merge only after required review and passing checks. Then update local `main`.

## TTG-14 to TTG-18 tracking

| Jira story | Scope | Estimate |
|---|---|---:|
| TTG-14 | Filterable timetable views (section, faculty, room) | 8 |
| TTG-15 | Drag-and-drop editor with conflict validation | 8 |
| TTG-16 | PDF and Excel export | 5 |
| TTG-17 | Async generation, health/uptime plumbing, audit, accessibility work | 8 |
| TTG-18 | TLS configuration, authentication/roles, password hashing, validation and rate limits | 8 |

Total: 37 points. Stories TTG-17 and TTG-18 span more than one contributor; Jira is the source of truth for actual assignments and completion. Do not infer individual contributions from this summary. Link each PR to the corresponding Jira item and retain review/check evidence.

## Submission accuracy

Keep the test matrix and deviation record aligned with the actual code and fresh test run. Do not report deployment uptime, formal WCAG conformance, production-grade security, or test coverage percentages unless measured and supported by evidence. See `docs/CHECKLIST_STATUS.md` for remaining evidence.
