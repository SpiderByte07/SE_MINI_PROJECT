import dataclasses
import pytest
from app.solver import Course, Faculty, Problem, Room, Section
from app.services.sample_data import demo_problem


def test_models_are_immutable():
    with pytest.raises(dataclasses.FrozenInstanceError):
        Room("LH-101", 60).capacity = 10


def test_problem_defaults():
    p = Problem([], [], [], [])
    assert (p.days, p.periods, p.timeout_seconds) == (5, 6, 15.0)


def test_tc_res_03_room_capacity_validated_on_entry():
    with pytest.raises(ValueError, match="capacity"):
        Room("LH-101", 0)


def test_section_enrollment_and_semester_validated():
    with pytest.raises(ValueError):
        Section("A", 0)
    with pytest.raises(ValueError):
        Section("A", 50, semester=9)


def test_course_rules_from_srs():
    with pytest.raises(ValueError, match="lab"):
        Course("L1", "A", "F1", 1, True, 1)        # labs need 2 or 3 contiguous periods
    with pytest.raises(ValueError):
        Course("C1", "A", "F1", 0)                 # weekly hours must be positive
    assert Course("CS101", "A", "F1", 3).credits == 3


def test_faculty_hours_validated():
    with pytest.raises(ValueError):
        Faculty("F1", max_hours_per_week=0)


def test_demo_problem_is_consistent():
    p = demo_problem()
    assert len(p.sections) == 2 and len(p.courses) == 6
    assert {c.faculty_id for c in p.courses} <= {f.id for f in p.faculty}
