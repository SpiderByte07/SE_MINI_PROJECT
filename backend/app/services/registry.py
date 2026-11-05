"""Resource registry: create / update / delete for Courses, Faculty, Rooms and
Sections (SRS TT-F-001..004).  In-memory for now; a database layer can replace it."""
from app.solver.models import Course, Faculty, Room, Section, Problem


class RegistryError(Exception):
    pass


class DuplicateError(RegistryError):
    pass


class NotFoundError(RegistryError):
    pass


class IntegrityError(RegistryError):
    pass


_TYPES = {"course": Course, "faculty": Faculty, "room": Room, "section": Section}


class ResourceRegistry:
    def __init__(self):
        self._data = {k: {} for k in _TYPES}

    @staticmethod
    def _key(kind, obj):
        return (obj.code, obj.section_id) if kind == "course" else obj.id

    def _check(self, kind, obj):
        if kind not in _TYPES:
            raise KeyError(f"Unknown resource kind: {kind}")
        if not isinstance(obj, _TYPES[kind]):
            raise TypeError(f"Expected {_TYPES[kind].__name__} for kind '{kind}'.")
        if kind == "course":  # a course must link to existing faculty and section
            if obj.faculty_id not in self._data["faculty"]:
                raise NotFoundError(f"Faculty {obj.faculty_id} does not exist.")
            if obj.section_id not in self._data["section"]:
                raise NotFoundError(f"Section {obj.section_id} does not exist.")

    def create(self, kind, obj):
        self._check(kind, obj)
        key = self._key(kind, obj)
        if key in self._data[kind]:
            raise DuplicateError(f"{kind} {key} already exists.")
        self._data[kind][key] = obj
        return obj

    def update(self, kind, obj):
        self._check(kind, obj)
        key = self._key(kind, obj)
        if key not in self._data[kind]:
            raise NotFoundError(f"{kind} {key} does not exist.")
        self._data[kind][key] = obj
        return obj

    def delete(self, kind, key):
        if key not in self._data[kind]:
            raise NotFoundError(f"{kind} {key} does not exist.")
        if kind in ("faculty", "section"):
            field_name = "faculty_id" if kind == "faculty" else "section_id"
            if any(getattr(c, field_name) == key for c in self._data["course"].values()):
                raise IntegrityError(f"{kind} {key} is still used by a course.")
        del self._data[kind][key]

    def get(self, kind, key):
        try:
            return self._data[kind][key]
        except KeyError:
            raise NotFoundError(f"{kind} {key} does not exist.") from None

    def list(self, kind):
        return list(self._data[kind].values())

    def to_problem(self, **kwargs) -> Problem:
        return Problem(courses=self.list("course"), faculty=self.list("faculty"),
                       rooms=self.list("room"), sections=self.list("section"), **kwargs)
