"""Cheap pre-checks that explain *why* a problem is infeasible (TT-F-010)."""
from .models import Problem


def diagnose(p: Problem) -> list:
    msgs = []
    slots = p.days * p.periods
    fac = {f.id: f for f in p.faculty}
    sec = {s.id: s for s in p.sections}

    sec_hours, fac_hours = {}, {}
    lab_hours = 0
    theory_hours = 0
    for c in p.courses:
        h = c.sessions_per_week * (c.block_length if c.is_lab else 1)
        sec_hours[c.section_id] = sec_hours.get(c.section_id, 0) + h
        fac_hours[c.faculty_id] = fac_hours.get(c.faculty_id, 0) + h
        if c.is_lab:
            lab_hours += h
        else:
            theory_hours += h
        if c.is_lab and c.block_length > p.periods:
            msgs.append(f"Course {c.code}: lab block longer than a day.")
        if c.faculty_id not in fac:
            msgs.append(f"Course {c.code}: unknown faculty {c.faculty_id}.")
        if c.section_id not in sec:
            msgs.append(f"Course {c.code}: unknown section {c.section_id}.")
            continue
        fits = [r for r in p.rooms if r.is_lab == c.is_lab and r.capacity >= sec[c.section_id].strength]
        if not fits:
            msgs.append(f"Course {c.code}: no {'lab' if c.is_lab else 'classroom'} "
                        f"with capacity >= {sec[c.section_id].strength}.")
    for s, h in sec_hours.items():
        if h > slots:
            msgs.append(f"Section {s}: needs {h} hours but only {slots} slots exist.")
    for f, h in fac_hours.items():
        if f in fac:
            avail = slots - len(fac[f].unavailable)
            if h > fac[f].max_hours_per_week:
                msgs.append(f"Faculty {f}: assigned {h}h exceeds max {fac[f].max_hours_per_week}h.")
            if h > avail:
                msgs.append(f"Faculty {f}: needs {h}h but only {avail} available slots.")
    n_lab = sum(r.is_lab for r in p.rooms)
    n_class = len(p.rooms) - n_lab
    if lab_hours > n_lab * slots:
        msgs.append(f"Labs: {lab_hours}h required > {n_lab * slots}h of lab room capacity.")
    if theory_hours > n_class * slots:
        msgs.append(f"Classrooms: {theory_hours}h required > {n_class * slots}h of room capacity.")
    return msgs
