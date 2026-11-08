from app.solver import Pin, solve
from app.services.sample_data import demo_problem


def test_tc_mod_02_pinned_slot_is_preserved():
    p = demo_problem()
    p.pins = [Pin("CS301", "A", 0, 0)]
    r = solve(p)
    assert any(a.course_code == "CS301" and a.section_id == "A"
               and a.day == 0 and a.period == 0 for a in r.assignments)


def test_unplaceable_pin_is_reported_infeasible():
    p = demo_problem()
    p.pins = [Pin("CS302L", "A", 0, 5)]     # a 2-period lab cannot start in the last period
    r = solve(p)
    assert r.status == "INFEASIBLE" and r.diagnostics
