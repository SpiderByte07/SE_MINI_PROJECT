"""Independent checker (SRS AC-TT-F-005..007): counts hard-constraint violations."""
from collections import Counter


def count_clashes(assignments) -> dict:
    fac, room, sec = Counter(), Counter(), Counter()
    for a in assignments:
        for k in range(a.length):
            cell = (a.day, a.period + k)
            fac[a.faculty_id, cell] += 1
            room[a.room_id, cell] += 1
            sec[a.section_id, cell] += 1
    f = lambda c: sum(v - 1 for v in c.values() if v > 1)
    return {"faculty": f(fac), "room": f(room), "section": f(sec)}
