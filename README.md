# College Timetable Generation System

Automatically assigns subjects, faculty, classrooms, laboratories and student sections
to weekly slots using Google OR-Tools CP-SAT, satisfying hard constraints (no faculty,
room or section clashes) and reporting why a timetable is infeasible when it is.

## Team

| Name | SRN |
|---|---|
| Saathvik Sai Suvarna | PES1UG24AM238 |
| Ayush PM | PES1UG24AM909 |
| Rishi Bharadwaj | PES1UG24AM223 |
| Rohit Chaki | PES1UG24AM228 |

## Repository layout
```
backend/
  app/
    solver/            CP-SAT model, infeasibility diagnostics, clash verifier
    services/          Sample data / application logic
    models/            Persistence models (to be added)
    export/            PDF / Excel export (to be added)
    cli.py             Command-line demo
  tests/
    unit/              Tests named after STP IDs (TC-xxx-nn)
.github/workflows/ci.yml   CI: runs pytest on every PR and push to main
requirements.txt  LICENSE  .gitignore  pytest.ini
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
cd backend && python -m app.cli      # demo run (available once all feature branches are merged)
```

## Workflow for every feature
```
main -> git pull -> feature/<name> -> add code + test -> pytest
     -> git add . -> git commit -> git push
     -> Pull Request -> main -> GitHub Actions: test passes
     -> 1 teammate approval -> merge -> everyone pulls main
```
Rules:
- `main` is protected: no direct pushes; PR + 1 approval + passing CI required.
- Every feature is developed on its own branch and has an appropriate test case.
- Run `pytest` locally before pushing.
- After every merge, everyone runs `git checkout main && git pull`.

See CONTRIBUTING.md for branch ownership and the ruleset settings.