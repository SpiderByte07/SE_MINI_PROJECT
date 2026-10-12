# College Timetable Generation System

Automatically assigns subjects, faculty, classrooms, laboratories and student sections
to weekly slots using Google OR-Tools CP-SAT, satisfying hard constraints (no faculty,
room or section clashes) and reporting why a timetable is infeasible when it is.

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
```
git clone https://github.com/<owner>/<repo>.git
cd <repo>
python -m venv .venv
.venv\Scripts\activate          # Windows   (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
pytest
cd backend && python -m app.cli      # demo run
```

## Workflow for every feature
```
main -> git pull -> feature/<name> -> add code + test -> pytest
     -> git add . -> git commit -> git push
     -> Pull Request -> main -> GitHub Actions: test passes
     -> 1 teammate approval -> merge -> everyone pulls main
```
See CONTRIBUTING.md for the branch ruleset settings and ownership.
