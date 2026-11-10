"""CP-SAT timetable model - hard constraints (SRS TT-F-005..009, TT-F-002) soft constraints (TT-F-011) and pinned slots (TT-F-014)."""
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

    fac = {f.id: f for f in p.faculty}
    sec = {s.id: s for s in p.sections}
    m = cp_model.CpModel()

    # start[i, d, t, room] == 1  <=>  course i is held at day d, period t, in that room
    start = {}
    cover = defaultdict(list)       # (kind, id, d, t) -> literals that use that cell
    per_course = defaultdict(list)
    per_course_day = defaultdict(list)
    sec_theory = defaultdict(list)   # theory literals per (section, day, period)

    for i, c in enumerate(p.courses):
        L = c.block_length if c.is_lab else 1                 # TT-F-008: a lab is 2 or 3 consecutive periods
        # TT-F-007/008: room seats the whole section; labs only in lab rooms, theory only in classrooms
        rooms = [r for r in p.rooms if r.is_lab == c.is_lab and r.capacity >= sec[c.section_id].strength]
        blocked = fac[c.faculty_id].unavailable              # TT-F-002: leave / blocked slots
        for d in range(p.days):
            for t in range(p.periods - L + 1):                # a block never runs past the end of the day
                cells = [(d, t + k) for k in range(L)]
                if any(cell in blocked for cell in cells):
                    continue                                      # prune impossible starts
                for r in rooms:
                    v = m.NewBoolVar(f"s_{i}_{d}_{t}_{r.id}")
                    start[i, d, t, r.id] = v
                    per_course[i].append(v)
                    per_course_day[i, d].append(v)
                    for (dd, tt) in cells:
                        cover["room", r.id, dd, tt].append(v)
                        cover["fac", c.faculty_id, dd, tt].append(v)
                        cover["sec", c.section_id, dd, tt].append(v)
                        if not c.is_lab:
                            sec_theory[c.section_id, dd, tt].append(v)

    for i, c in enumerate(p.courses):
        m.Add(sum(per_course[i]) == c.sessions_per_week)      # every required hour is placed
        for d in range(p.days):                               # at most one block of a course per day
            if per_course_day[i, d]:
                m.Add(sum(per_course_day[i, d]) <= 1)
    for lits in cover.values():                               # TT-F-005/006/007: nothing is double-booked
        if len(lits) > 1:
            m.AddAtMostOne(lits)

    # TT-F-014: pinned slots stay fixed
    for pin in p.pins:
        idx = [i for i, c in enumerate(p.courses)
               if c.code == pin.course_code and c.section_id == pin.section_id]
        lits = [v for (i, d, t, _), v in start.items()
                if i in idx and d == pin.day and t == pin.period]
        if not lits:
            return Result("INFEASIBLE", diagnostics=[f"Pin for {pin.course_code} is not placeable."],
                          runtime_seconds=time.time() - t0)
        m.Add(sum(lits) == 1)

    # TT-F-011 (a): minimise faculty idle gaps between lectures on the same day
    penalties = []
    for f in fac:
        for d in range(p.days):
            occ = [cover.get(("fac", f, d, t), []) for t in range(p.periods)]
            if not any(occ):
                continue
            before = [m.NewBoolVar(f"b_{f}_{d}_{t}") for t in range(p.periods)]
            after = [m.NewBoolVar(f"a_{f}_{d}_{t}") for t in range(p.periods)]
            for t in range(p.periods):
                if t > 0:
                    m.Add(before[t] >= sum(occ[t - 1]))
                    m.Add(before[t] >= before[t - 1])
                else:
                    m.Add(before[0] == 0)
                if t < p.periods - 1:
                    m.Add(after[t] >= sum(occ[t + 1]))
                    m.Add(after[t] >= after[t + 1])
                else:
                    m.Add(after[t] == 0)
                idle = m.NewBoolVar(f"i_{f}_{d}_{t}")
                m.Add(idle >= before[t] + after[t] - 1 - sum(occ[t]))
                penalties.append(idle)

    # TT-F-011 (b): avoid heavy theory runs - 3 consecutive theory periods for a section
    for sid in sec:
        for d in range(p.days):
            for t in range(p.periods - 2):
                w = [sec_theory.get((sid, d, t + k), []) for k in range(3)]
                if all(w):
                    viol = m.NewBoolVar(f"h_{sid}_{d}_{t}")
                    m.Add(viol >= sum(w[0]) + sum(w[1]) + sum(w[2]) - 2)
                    penalties.append(viol)

    def left():
        return p.timeout_seconds - (time.time() - t0)

    # Phase 1: find ANY clash-free timetable quickly (hard constraints only) - SRS TT-NF-001
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = max(1.0, left())
    s.parameters.num_workers = 4
    status = s.Solve(m)
    if status == cp_model.INFEASIBLE:
        return Result("INFEASIBLE", [], ["No conflict-free timetable exists under current constraints."],
                      time.time() - t0)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return Result("TIMEOUT", [], [f"Solver stopped after {p.timeout_seconds}s without a solution."],
                      time.time() - t0)
    values = {key: s.Value(v) for key, v in start.items()}
    name = "OPTIMAL"
    penalty = 0

    # Phase 2: use the remaining time to reduce the soft penalty (TT-F-011), warm-started
    if penalties:
        name = "FEASIBLE"
        penalty = sum(s.Value(x) for x in penalties)      # upper bound if phase 2 cannot run
        if left() >= 1.0:
            for key, v in start.items():
                m.AddHint(v, values[key])
            m.Minimize(sum(penalties))
            s2 = cp_model.CpSolver()
            s2.parameters.max_time_in_seconds = left()
            s2.parameters.num_workers = 4
            st2 = s2.Solve(m)
            if st2 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                values = {key: s2.Value(v) for key, v in start.items()}
                penalty = int(round(s2.ObjectiveValue()))
                name = s2.StatusName(st2)

    out = []
    for (i, d, t, r), v in values.items():
        if v:
            c = p.courses[i]
            out.append(Assignment(c.code, c.section_id, c.faculty_id, r, d, t,
                                  c.block_length if c.is_lab else 1))
    return Result(name, out, [], time.time() - t0, penalty)
