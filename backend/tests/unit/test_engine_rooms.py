from app.solver import solve
from app.services.sample_data import demo_problem


def test_tc_cst_03_room_capacity_respected():
    p = demo_problem()
    caps = {r.id: r.capacity for r in p.rooms}
    strengths = {s.id: s.strength for s in p.sections}
    result = solve(p)
    assert result.assignments
    for a in result.assignments:
        assert caps[a.room_id] >= strengths[a.section_id]


def test_theory_in_classrooms_and_labs_in_lab_rooms():
    p = demo_problem()
    lab_rooms = {r.id for r in p.rooms if r.is_lab}
    is_lab = {(c.code, c.section_id): c.is_lab for c in p.courses}
    for a in solve(p).assignments:
        assert (a.room_id in lab_rooms) == is_lab[(a.course_code, a.section_id)]
