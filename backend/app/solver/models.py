"""Domain entities with the attributes required by SRS TT-F-001..004,
plus the solver input/output containers."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Faculty:                      # TT-F-002
    id: str
    max_hours_per_week: int = 20
    unavailable: frozenset = frozenset()        # {(day, period)} leave / blocked slots
    assigned_subjects: frozenset = frozenset()  # course codes this faculty may teach

    def __post_init__(self):
        if self.max_hours_per_week <= 0:
            raise ValueError(f"Faculty {self.id}: max hours per week must be positive.")


@dataclass(frozen=True)
class Room:                         # TT-F-003 (id doubles as room number)
    id: str
    capacity: int
    is_lab: bool = False
    equipment: frozenset = frozenset()          # supported equipment flags

    def __post_init__(self):
        if self.capacity <= 0:
            raise ValueError(f"Room {self.id}: seating capacity must be positive.")


@dataclass(frozen=True)
class Section:                      # TT-F-004
    id: str
    strength: int
    semester: int = 1
    required_courses: tuple = ()                # course codes required by this section

    def __post_init__(self):
        if self.strength <= 0:
            raise ValueError(f"Section {self.id}: enrollment count must be positive.")
        if not 1 <= self.semester <= 8:
            raise ValueError(f"Section {self.id}: semester must be between 1 and 8.")


@dataclass(frozen=True)
class Course:                       # TT-F-001
    code: str
    section_id: str
    faculty_id: str
    sessions_per_week: int          # weekly lecture hours (theory) / number of blocks (lab)
    is_lab: bool = False            # course type: Theory vs Practical
    block_length: int = 1           # labs: 2 or 3 contiguous periods (TT-F-008)
    credits: int = 3

    def __post_init__(self):
        if self.sessions_per_week <= 0:
            raise ValueError(f"Course {self.code}: weekly hours must be positive.")
        if self.credits <= 0:
            raise ValueError(f"Course {self.code}: credits must be positive.")
        if self.is_lab and self.block_length not in (2, 3):
            raise ValueError(f"Course {self.code}: lab blocks must be 2 or 3 consecutive periods.")
        if not self.is_lab and self.block_length != 1:
            raise ValueError(f"Course {self.code}: theory sessions occupy a single period.")


@dataclass(frozen=True)
class Pin:                          # TT-F-014
    course_code: str
    section_id: str
    day: int
    period: int


@dataclass
class Problem:
    courses: list
    faculty: list
    rooms: list
    sections: list
    days: int = 5
    periods: int = 6
    pins: list = field(default_factory=list)
    timeout_seconds: float = 15.0


@dataclass(frozen=True)
class Assignment:
    course_code: str
    section_id: str
    faculty_id: str
    room_id: str
    day: int
    period: int
    length: int


@dataclass
class Result:
    status: str                     # OPTIMAL | FEASIBLE | INFEASIBLE | TIMEOUT
    assignments: list = field(default_factory=list)
    diagnostics: list = field(default_factory=list)
    runtime_seconds: float = 0.0
    soft_penalty: int = 0           # UC-GEN-01: soft penalty score
