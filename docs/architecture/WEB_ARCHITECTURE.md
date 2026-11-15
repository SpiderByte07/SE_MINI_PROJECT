# Web Architecture Supplement for the SAD

This supplement describes the merged demo web layer. It is intended to accompany the approved SAD and can be incorporated into its architecture diagrams if the course requires a single revised PDF.

## Component view

```mermaid
flowchart LR
    User[Coordinator / viewer] --> Browser[Browser UI<br/>backend/app/web/frontend/index.html]
    Browser -->|HTTPS when deployed through trusted proxy| API[FastAPI app<br/>web/main.py]
    API --> Auth[Security dependencies<br/>web/security.py]
    API --> Schedule[Schedule routes<br/>web/schedule.py]
    API --> Export[Export routes<br/>web/reports.py]
    API --> Jobs[Generation routes<br/>web/generation.py]
    API --> Health[Health route<br/>web/health.py]
    API --> Audit[Audit service<br/>web/audit.py]
    Schedule --> Sample[Demo sample data]
    Jobs --> Solver[OR-Tools solver<br/>app/solver]
    Sample --> Solver
    Jobs --> Schedule
    Audit --> SQLite[(Local SQLite audit file)]
```

## Async generation sequence

```mermaid
sequenceDiagram
    actor Coordinator
    participant UI as Browser UI
    participant API as FastAPI generation route
    participant Worker as Background thread
    participant Solver as OR-Tools solver
    participant Audit as SQLite audit
    Coordinator->>UI: Request timetable generation
    UI->>API: POST /api/generate with bearer token
    API->>API: Check coordinator role and request limit
    API-->>UI: 202 Accepted with job_id
    API->>Worker: Start solver task
    Worker->>Solver: Solve demo problem
    Solver-->>Worker: Status, assignments, diagnostics
    Worker->>API: Save job result in process memory
    Worker->>Audit: Record generation result
    UI->>API: GET /api/jobs/{job_id}
    API-->>UI: Current job status/result
```

## Schedule move sequence

```mermaid
sequenceDiagram
    actor Coordinator
    participant UI as Browser UI
    participant API as FastAPI schedule route
    participant Security as Auth/role dependency
    participant Audit as SQLite audit
    Coordinator->>UI: Drag class to another slot
    UI->>API: PUT /api/schedule/{entry_id}
    API->>Security: Validate bearer token and coordinator role
    Security-->>API: Authorized / denied
    API->>API: Validate bounds and section/faculty/room conflicts
    alt Valid move
        API->>API: Update in-memory schedule
        API->>Audit: Record move
        API-->>UI: 200 Updated assignment
    else Invalid move
        API-->>UI: 409 Conflict or 422 invalid input
    end
```

## Deployment and persistence limits

The demo schedule and async job map are process-local. Audit events use a local SQLite file. HTTPS is enforced only when configured behind a trusted TLS proxy. These diagrams describe the current code; they do not claim durable jobs, multi-instance coordination, deployed uptime, or production security certification.
