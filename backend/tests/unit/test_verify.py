from app.solver import Assignment
from app.solver.verify import count_clashes


def A(code, sec, fac, room, day, period, length=1):
    return Assignment(code, sec, fac, room, day, period, length)


def test_clean_schedule_has_zero_clashes():
    s = [A("C1", "A", "F1", "R1", 0, 0), A("C2", "B", "F2", "R2", 0, 0)]
    assert count_clashes(s) == {"faculty": 0, "room": 0, "section": 0}


def test_detects_faculty_room_and_section_clash():
    s = [A("C1", "A", "F1", "R1", 0, 0), A("C2", "A", "F1", "R1", 0, 0)]
    assert count_clashes(s) == {"faculty": 1, "room": 1, "section": 1}


def test_multi_period_block_overlap_detected():
    s = [A("L1", "A", "F1", "LAB", 1, 2, 2), A("C1", "B", "F2", "LAB", 1, 3)]
    assert count_clashes(s)["room"] == 1
