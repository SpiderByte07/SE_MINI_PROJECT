"""Real-time validation of a manual slot move (SRS TT-F-013 / SAD 'Schedule Validation Service').
Returns a list of conflicts; an empty list means the move is allowed."""


def validate_move(problem, assignments, entry, day, period, room_id) -> list:
    conflicts = []

    def add(kind, msg):
        conflicts.append({"conflict_type": kind, "message": msg})

    course = next((c for c in problem.courses
                   if c.code == entry.course_code and c.section_id == entry.section_id), None)
    if course is None:
        add("UNKNOWN_COURSE", f"Course {entry.course_code} / section {entry.section_id} not found.")
        return conflicts
    if not (0 <= day < problem.days) or period < 0 or period + entry.length > problem.periods:
        add("OUT_OF_RANGE", "Target slot lies outside the weekly grid.")
        return conflicts
    room = next((r for r in problem.rooms if r.id == room_id), None)
    if room is None:
        add("UNKNOWN_ROOM", f"Room {room_id} not found.")
        return conflicts

    section = next(s for s in problem.sections if s.id == entry.section_id)
    faculty = next(f for f in problem.faculty if f.id == entry.faculty_id)
    cells = {(day, period + k) for k in range(entry.length)}
    where = f"day {day} period {period + 1}"

    if room.is_lab != course.is_lab:
        add("ROOM_TYPE", f"Room {room_id} is not a suitable {'lab' if course.is_lab else 'classroom'}.")
    if room.capacity < section.strength:
        add("ROOM_CAPACITY", f"Room {room_id} seats {room.capacity} but section "
                             f"{section.id} has {section.strength} students.")
    if cells & set(faculty.unavailable):
        add("FACULTY_UNAVAILABLE", f"Faculty {faculty.id} is unavailable at {where}.")

    for other in assignments:
        if other == entry:
            continue
        other_cells = {(other.day, other.period + k) for k in range(other.length)}
        if not cells & other_cells:
            continue
        if other.faculty_id == entry.faculty_id:
            add("FACULTY_DOUBLE_BOOKING", f"Faculty '{entry.faculty_id}' is already assigned to "
                                          f"'{other.section_id}' in room '{other.room_id}' at {where}.")
        if other.room_id == room_id:
            add("ROOM_DOUBLE_BOOKING", f"Room '{room_id}' is already used by "
                                       f"'{other.section_id}' at {where}.")
        if other.section_id == entry.section_id:
            add("SECTION_DOUBLE_BOOKING", f"Section '{entry.section_id}' already has "
                                          f"'{other.course_code}' at {where}.")
    return conflicts
