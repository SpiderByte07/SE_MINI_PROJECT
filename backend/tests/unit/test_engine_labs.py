from app.solver import solve
from app.solver.verify import count_clashes
from app.services.sample_data import demo_problem


def lab_assignments():
    return [a for a in solve(demo_problem()).assignments if a.course_code == "CS302L"]


def test_tc_cst_04_lab_blocks_are_contiguous_in_lab_rooms():
    labs = lab_assignments()
    assert len(labs) == 2
    assert all(a.length == 2 and a.room_id == "LAB-1" for a in labs)


def test_lab_block_never_splits_across_days():
    assert all(a.period + a.length <= 6 for a in lab_assignments())


def test_multi_period_blocks_stay_clash_free():
    r = solve(demo_problem())
    assert count_clashes(r.assignments) == {"faculty": 0, "room": 0, "section": 0}
