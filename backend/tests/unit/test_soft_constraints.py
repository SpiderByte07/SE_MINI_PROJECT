from collections import defaultdict
from app.solver import Course, Faculty, Problem, Room, Section, solve
from app.services.sample_data import demo_problem


def idle_gaps(assignments):
    cells = defaultdict(set)
    for a in assignments:
        for k in range(a.length):
            cells[a.faculty_id, a.day].add(a.period + k)
    return sum(max(c) - min(c) + 1 - len(c) for c in cells.values())


def test_tc_gen_03_faculty_idle_gaps_are_minimised():
    r = solve(demo_problem())
    assert r.status in ("OPTIMAL", "FEASIBLE")
    assert idle_gaps(r.assignments) == 0 and r.soft_penalty == 0


def test_soft_penalty_counts_unavoidable_idle_periods():
    p = Problem(
        courses=[Course("X", "A", "F1", 1), Course("Y", "A", "F1", 1)],
        faculty=[Faculty("F1", unavailable=frozenset({(0, 1), (0, 2), (0, 3), (0, 4)}))],
        rooms=[Room("LH-1", 60)], sections=[Section("A", 55)], days=1, periods=6)
    r = solve(p)
    assert r.status in ("OPTIMAL", "FEASIBLE") and r.soft_penalty == 4
