# College Timetable Generation System

Automatically assigns subjects, faculty, classrooms, laboratories and student sections
to available weekly slots while satisfying constraints and avoiding conflicts.
The planned solver uses Google OR-Tools CP-SAT to guarantee zero faculty, room and
section double-bookings, and to report why a timetable is infeasible when it is.

## Team

| Name | SRN |
|---|---|
| Saathvik Sai Suvarna | PES1UG24AM238 |
| Ayush PM | PES1UG24AM909 |
| Rishi Bharadwaj | PES1UG24AM223 |
| Rohit Chaki | PES1UG24AM228 |

## Phase 1 documents

| Document | File |
|---|---|
| Software Requirements Specification (SRS) | [SRS_College_Timetable_Generation_System.pdf](SRS_College_Timetable_Generation_System.pdf) |
| Software Architecture and Design (SAD) | [SAD_College_Timetable_Generation_System.pdf](SAD_College_Timetable_Generation_System.pdf) |
| Software Test Plan (STP) | [STP_College_Timetable_Generation_System.pdf](STP_College_Timetable_Generation_System.pdf) |

## Repository layout
```
.github/workflows/ci.yml   CI: runs pytest on every pull request and push to main
backend/
  app/                     Application package (solver, services, models, export to be added)
  tests/unit/              Unit tests (named after STP test case IDs)
*.pdf                      Phase 1 documents (SRS, SAD, STP)
requirements.txt  pytest.ini  LICENSE  .gitignore  CONTRIBUTING.md
```

## Team setup (once per teammate)
Clone the repository directly (do not fork):
```
git clone https://github.com/SpiderByte07/SE_MINI_PROJECT.git
cd SE_MINI_PROJECT
python -m venv .venv
.venv\Scripts\activate          # Windows   (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
pytest
```

## Workflow for every change
```
main -> git pull -> feature/<name> -> add code + test -> pytest
     -> git add . -> git commit -> git push
     -> Pull Request -> main -> GitHub Actions: test passes
     -> 1 teammate approval -> merge -> everyone pulls main
```
Rules:
- `main` is protected: no direct pushes; a PR, 1 approval and passing CI are required.
- Every feature is developed on its own branch and has an appropriate test case.
- Run `pytest` locally before pushing.
- After every merge, everyone runs `git checkout main && git pull`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full team workflow.