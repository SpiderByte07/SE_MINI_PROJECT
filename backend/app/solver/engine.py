"""CP-SAT timetable model - stage TTG-7: + room capacity and lab / classroom matching (SRS TT-F-007, TT-F-008)."""
import time
from collections import defaultdict
from ortools.sat.python import cp_model
from .models import Problem, Assignment, Result


def solve(p: Problem) -> Result:
    t0 = time.time()
    sec = {s.id: s for s in p.sections}
    m = cp_model.CpModel()

    # start[i, d, t, room] == 1  <=>  course i is held at day d, period t, in that room
    start = {}
    cover = defaultdict(list)       # (kind, id, d, t) -> literals that use that cell
    per_course = defaultdict(list)

    for i, c in enumerate(p.courses):
        # TT-F-007/008: room seats the whole section; labs only in lab rooms, theory only in classrooms
        rooms = [r for r in p.rooms if r.is_lab == c.is_lab and r.capacity >= sec[c.section_id].strength]
        for d in range(p.days):
            for t in range(p.periods):
                for r in rooms:
                    v = m.NewBoolVar(f"s_{i}_{d}_{t}_{r.id}")
                    start[i, d, t, r.id] = v
                    per_course[i].append(v)
                    cover["room", r.id, d, t].append(v)
                    cover["fac", c.faculty_id, d, t].append(v)
                    cover["sec", c.section_id, d, t].append(v)

    for i, c in enumerate(p.courses):
        m.Add(sum(per_course[i]) == c.sessions_per_week)      # every required hour is placed
    for lits in cover.values():                               # TT-F-005/006/007: nothing is double-booked
        if len(lits) > 1:
            m.AddAtMostOne(lits)

    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = p.timeout_seconds
    status = s.Solve(m)
    elapsed = time.time() - t0

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        out = []
        for (i, d, t, r), v in start.items():
            if s.Value(v):
                c = p.courses[i]
                out.append(Assignment(c.code, c.section_id, c.faculty_id, r, d, t, 1))
        return Result(s.StatusName(status), out, [], elapsed)
    return Result("INFEASIBLE" if status == cp_model.INFEASIBLE else "TIMEOUT", [], [], elapsed)
