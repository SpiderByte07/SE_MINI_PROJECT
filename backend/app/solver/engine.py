"""CP-SAT timetable model - stage TTG-9: + complete weekly generation with diagnostics and time limit (SRS TT-F-009, TT-F-010)."""
import time
from collections import defaultdict
from ortools.sat.python import cp_model
from .models import Problem, Assignment, Result
from .diagnostics import diagnose


def solve(p: Problem) -> Result:
    t0 = time.time()
    issues = diagnose(p)                                      # explain impossible inputs up front
    if issues:
        return Result("INFEASIBLE", diagnostics=issues, runtime_seconds=time.time() - t0)

    sec = {s.id: s for s in p.sections}
    m = cp_model.CpModel()

    # start[i, d, t, room] == 1  <=>  course i is held at day d, period t, in that room
    start = {}
    cover = defaultdict(list)       # (kind, id, d, t) -> literals that use that cell
    per_course = defaultdict(list)
    per_course_day = defaultdict(list)

    for i, c in enumerate(p.courses):
        L = c.block_length if c.is_lab else 1                 # TT-F-008: a lab is 2 or 3 consecutive periods
        # TT-F-007/008: room seats the whole section; labs only in lab rooms, theory only in classrooms
        rooms = [r for r in p.rooms if r.is_lab == c.is_lab and r.capacity >= sec[c.section_id].strength]
        for d in range(p.days):
            for t in range(p.periods - L + 1):                # a block never runs past the end of the day
                cells = [(d, t + k) for k in range(L)]
                for r in rooms:
                    v = m.NewBoolVar(f"s_{i}_{d}_{t}_{r.id}")
                    start[i, d, t, r.id] = v
                    per_course[i].append(v)
                    per_course_day[i, d].append(v)
                    for (dd, tt) in cells:
                        cover["room", r.id, dd, tt].append(v)
                        cover["fac", c.faculty_id, dd, tt].append(v)
                        cover["sec", c.section_id, dd, tt].append(v)

    for i, c in enumerate(p.courses):
        m.Add(sum(per_course[i]) == c.sessions_per_week)      # every required hour is placed
        for d in range(p.days):                               # at most one block of a course per day
            if per_course_day[i, d]:
                m.Add(sum(per_course_day[i, d]) <= 1)
    for lits in cover.values():                               # TT-F-005/006/007: nothing is double-booked
        if len(lits) > 1:
            m.AddAtMostOne(lits)

    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = max(1.0, p.timeout_seconds - (time.time() - t0))
    s.parameters.num_workers = 4
    status = s.Solve(m)
    elapsed = time.time() - t0

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        out = []
        for (i, d, t, r), v in start.items():
            if s.Value(v):
                c = p.courses[i]
                out.append(Assignment(c.code, c.section_id, c.faculty_id, r, d, t,
                                      c.block_length if c.is_lab else 1))
        return Result(s.StatusName(status), out, [], elapsed)
    if status == cp_model.INFEASIBLE:
        return Result("INFEASIBLE", [], ["No conflict-free timetable exists under current constraints."], elapsed)
    return Result("TIMEOUT", [], [f"Solver stopped after {p.timeout_seconds}s without a solution."], elapsed)
