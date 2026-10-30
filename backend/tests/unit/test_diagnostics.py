from app.solver import Course, Section
from app.solver.diagnostics import diagnose
from app.services.sample_data import demo_problem


def test_clean_problem_has_no_diagnostics():
    assert diagnose(demo_problem()) == []


def test_tc_gen_02_overloaded_week_reports_bottleneck():
    p = demo_problem()
    p.courses.append(Course("X", "A", "F1", 50))   # 50h in a 30-slot week
    msgs = diagnose(p)
    assert any("Section A" in m for m in msgs) and any("Faculty F1" in m for m in msgs)


def test_room_capacity_shortfall_is_named():
    p = demo_problem()
    p.sections[0] = Section("A", 500)
    assert any("capacity" in m for m in diagnose(p))


def test_unknown_faculty_is_reported():
    p = demo_problem()
    p.courses.append(Course("Y", "A", "NOPE", 1))
    assert any("unknown faculty" in m for m in diagnose(p))
