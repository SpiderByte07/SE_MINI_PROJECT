from app.solver import Course, Faculty, Problem, Room, Section, solve
from app.solver.verify import count_clashes


def synthetic_problem(n_sections=30):
    sections = [Section(f"S{i}", 55, 5) for i in range(n_sections)]
    faculty = [Faculty(f"T{i}") for i in range(24)] + [Faculty(f"L{i}") for i in range(6)]
    courses = []
    for i in range(n_sections):
        for k in range(4):
            courses.append(Course(f"TH{k}", f"S{i}", f"T{(i * 4 + k) % 24}", 3))
        courses.append(Course("LAB", f"S{i}", f"L{i % 6}", 1, True, 2))
    rooms = [Room(f"LH-{i}", 60) for i in range(20)] + [Room(f"LAB-{i}", 60, True) for i in range(6)]
    return Problem(courses, faculty, rooms, sections, timeout_seconds=12)


def test_tc_perf_01_thirty_sections_within_15_seconds():
    r = solve(synthetic_problem(30))
    assert r.status in ("OPTIMAL", "FEASIBLE")
    assert r.runtime_seconds <= 15
    assert count_clashes(r.assignments) == {"faculty": 0, "room": 0, "section": 0}
