from app.solver import Faculty, solve
from app.services.sample_data import demo_problem


def test_tc_res_02_blocked_slots_are_never_assigned():
    p = demo_problem()
    p.faculty[0] = Faculty("F1", unavailable=frozenset({(0, 0), (0, 1)}))
    result = solve(p)
    assert result.assignments
    for a in result.assignments:
        if a.faculty_id == "F1":
            assert not (a.day == 0 and a.period in (0, 1))


def test_whole_day_leave_is_respected():
    p = demo_problem()
    p.faculty[1] = Faculty("F2", unavailable=frozenset((2, t) for t in range(6)))
    for a in solve(p).assignments:
        if a.faculty_id == "F2":
            assert a.day != 2
