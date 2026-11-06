from collections import Counter
from app.solver import Course, solve
from app.solver.verify import count_clashes
from app.services.sample_data import demo_problem


def test_tc_gen_01_generates_complete_schedule():
    r = solve(demo_problem())
    assert r.status in ("OPTIMAL", "FEASIBLE")
    assert len(r.assignments) == 4 + 3 + 1 + 4 + 3 + 1


def test_generated_timetable_has_zero_clashes():
    r = solve(demo_problem())
    assert count_clashes(r.assignments) == {"faculty": 0, "room": 0, "section": 0}


def test_course_is_not_repeated_on_the_same_day():
    r = solve(demo_problem())
    per_day = Counter((a.course_code, a.section_id, a.day) for a in r.assignments)
    assert max(per_day.values()) == 1


def test_tc_gen_02_infeasible_problem_reports_diagnostics():
    p = demo_problem()
    p.courses.append(Course("X", "A", "F1", 50))    # 50 hours in a 30-slot week
    r = solve(p)
    assert r.status == "INFEASIBLE" and r.diagnostics and r.assignments == []


def test_runtime_is_reported():
    assert solve(demo_problem()).runtime_seconds >= 0
