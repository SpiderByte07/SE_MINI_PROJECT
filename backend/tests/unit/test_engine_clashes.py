from app.solver import solve
from app.solver.verify import count_clashes
from app.services.sample_data import demo_problem


def theory_only():
    p = demo_problem()
    p.courses = [c for c in p.courses if not c.is_lab]
    return p


def test_tc_cst_01_no_faculty_double_booking():
    r = solve(theory_only())
    assert r.status in ("OPTIMAL", "FEASIBLE")
    assert count_clashes(r.assignments)["faculty"] == 0


def test_tc_cst_02_no_room_collisions():
    assert count_clashes(solve(theory_only()).assignments)["room"] == 0


def test_tc_cst_03_no_section_clashes():
    assert count_clashes(solve(theory_only()).assignments)["section"] == 0


def test_all_required_sessions_are_placed():
    assert len(solve(theory_only()).assignments) == 4 + 3 + 4 + 3
