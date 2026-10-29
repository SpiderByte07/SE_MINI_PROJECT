"""Small demo dataset used by tests."""
from app.solver import Course, Room, Section, Faculty, Problem


def demo_problem(timeout: float = 15.0) -> Problem:
    return Problem(
        courses=[
            Course("CS301", "A", "F1", 4), Course("CS302", "A", "F2", 3),
            Course("CS302L", "A", "F3", 1, True, 2),
            Course("CS301", "B", "F1", 4), Course("CS302", "B", "F2", 3),
            Course("CS302L", "B", "F3", 1, True, 2),
        ],
        faculty=[Faculty("F1"), Faculty("F2"), Faculty("F3")],
        rooms=[Room("LH-101", 60), Room("LH-102", 60), Room("LAB-1", 70, True)],
        sections=[Section("A", 55, 5), Section("B", 58, 5)],
        timeout_seconds=timeout,
    )
