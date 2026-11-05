import pytest
from app.solver import Course, Faculty, Room, Section
from app.services.registry import (ResourceRegistry, DuplicateError, NotFoundError,
                                   IntegrityError)


def loaded():
    r = ResourceRegistry()
    r.create("faculty", Faculty("F1"))
    r.create("section", Section("A", 55, 5))
    r.create("room", Room("LH-101", 60))
    return r


def test_tc_res_01_course_created_and_persisted():
    r = loaded()
    r.create("course", Course("CS301", "A", "F1", 4, credits=4))
    c = r.get("course", ("CS301", "A"))
    assert c.sessions_per_week == 4 and c.credits == 4


def test_tc_res_02_faculty_unavailability_stored():
    r = ResourceRegistry()
    r.create("faculty", Faculty("FAC_01", unavailable=frozenset({(0, 0), (0, 1)})))
    assert (0, 1) in r.get("faculty", "FAC_01").unavailable


def test_update_course():
    r = loaded()
    r.create("course", Course("CS301", "A", "F1", 4))
    r.update("course", Course("CS301", "A", "F1", 3))
    assert r.get("course", ("CS301", "A")).sessions_per_week == 3


def test_delete_course_and_room():
    r = loaded()
    r.create("course", Course("CS301", "A", "F1", 4))
    r.delete("course", ("CS301", "A"))
    r.delete("room", "LH-101")
    assert r.list("course") == [] and r.list("room") == []


def test_duplicate_rejected():
    r = loaded()
    with pytest.raises(DuplicateError):
        r.create("room", Room("LH-101", 80))


def test_course_must_link_to_existing_faculty_and_section():
    r = loaded()
    with pytest.raises(NotFoundError):
        r.create("course", Course("CS301", "A", "NOPE", 4))
    with pytest.raises(NotFoundError):
        r.create("course", Course("CS301", "Z", "F1", 4))


def test_cannot_delete_faculty_or_section_in_use():
    r = loaded()
    r.create("course", Course("CS301", "A", "F1", 4))
    with pytest.raises(IntegrityError):
        r.delete("faculty", "F1")
    with pytest.raises(IntegrityError):
        r.delete("section", "A")


def test_to_problem_collects_everything():
    r = loaded()
    r.create("course", Course("CS301", "A", "F1", 4))
    p = r.to_problem(days=5, periods=6)
    assert len(p.courses) == 1 and len(p.rooms) == 1 and p.days == 5
