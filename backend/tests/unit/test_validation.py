from app.solver import Assignment, Faculty
from app.solver.validation import validate_move
from app.services.sample_data import demo_problem


def A(code, sec, fac, room, day, period, length=1):
    return Assignment(code, sec, fac, room, day, period, length)


def kinds(conflicts):
    return {c["conflict_type"] for c in conflicts}


def setup():
    a = A("CS301", "A", "F1", "LH-101", 0, 0)       # entry we will move
    b = A("CS301", "B", "F1", "LH-102", 1, 2)       # same faculty, Tue period 3
    c = A("CS302", "A", "F2", "LH-101", 2, 4)
    return demo_problem(), [a, b, c], a


def test_tc_mod_01_faculty_clash_is_rejected():
    p, s, a = setup()
    assert "FACULTY_DOUBLE_BOOKING" in kinds(validate_move(p, s, a, 1, 2, "LH-101"))


def test_valid_move_returns_no_conflicts():
    p, s, a = setup()
    assert validate_move(p, s, a, 3, 1, "LH-101") == []


def test_room_double_booking_detected():
    p, s, a = setup()
    assert "ROOM_DOUBLE_BOOKING" in kinds(validate_move(p, s, a, 2, 4, "LH-101"))


def test_section_double_booking_detected():
    p, s, a = setup()
    assert "SECTION_DOUBLE_BOOKING" in kinds(validate_move(p, s, a, 2, 4, "LH-102"))


def test_capacity_and_room_type_checked():
    p, s, a = setup()
    p.sections[0] = type(p.sections[0])("A", 65, 5)
    assert "ROOM_CAPACITY" in kinds(validate_move(p, s, a, 3, 1, "LH-101"))
    assert "ROOM_TYPE" in kinds(validate_move(p, s, a, 3, 1, "LAB-1"))


def test_faculty_unavailability_and_bounds_checked():
    p, s, a = setup()
    p.faculty[0] = Faculty("F1", unavailable=frozenset({(3, 1)}))
    assert "FACULTY_UNAVAILABLE" in kinds(validate_move(p, s, a, 3, 1, "LH-101"))
    assert kinds(validate_move(p, s, a, 9, 0, "LH-101")) == {"OUT_OF_RANGE"}
