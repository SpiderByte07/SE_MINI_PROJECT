# Team Workflow

## GitHub ruleset for `main` (Settings -> Rules -> Rulesets -> New branch ruleset)
- Enforcement status: **Active**; target branch: default branch (`main`)
- Require a pull request before merging, required approvals: **1**
- Require status checks to pass -> Add checks -> select `test` (appears after CI runs once)
- Block force pushes


1. One shared repo; all teammates are collaborators. **Clone, don't fork.**
2. `main` is protected: PR + 1 approval + passing CI required. No direct pushes.
3. One feature = one branch (`feature/<name>`), with tests named after STP IDs (TC-xxx-nn).
4. Run `pytest` locally before pushing.
5. Open a PR using the template; a teammate reviews; merge only when CI is green.
6. After every merge: `git checkout main && git pull`.
7. Keep contributions balanced; each member owns at least one module.

## Branch ownership (merge in this order)
| # | Branch | Adds | Owner |
|---|---|---|---|
| 1 | feature/solver-models | solver/models.py, solver/__init__.py, services/sample_data.py | |
| 2 | feature/diagnostics-and-verifier | solver/diagnostics.py, solver/verify.py | |
| 3 | feature/solver-engine | solver/engine.py (hard constraints), updates solver/__init__.py | |
| 4 | feature/pins-cli-perf | cli.py, pin + performance + CLI tests | |

Later (anyone): feature/resource-crud (models/), feature/export (export/), feature/soft-constraints (solver/).

## Where does my code go?
- Scheduling rules: `backend/app/solver/`
- Data / application logic: `backend/app/services/`
- DB entities: `backend/app/models/`  |  Export: `backend/app/export/`
- Tests: `backend/tests/unit/`, named after STP IDs
