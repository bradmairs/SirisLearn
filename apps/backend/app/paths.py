"""Learning paths: an ordered set of courses with an optional target date,
such as "AI leader" (How AI works, then Leading with AI in engineering
consulting).

A path's progress counts every lesson passed plus every final exam passed,
so a path is done when each course's lessons and exam are. With a target
date, the path is "on track" when progress is at least where a steady pace
from the start date would put it today (less a week's grace), otherwise
"behind", and it says how many lessons a week would still get there.

The built-in "AI leader" path is added once, when both AI courses are in
the library (deleting it keeps it deleted).
"""

from __future__ import annotations

import math
from datetime import date
from typing import Any

from app.db import Store, local_day, new_id, now_iso

BUILT_IN = [
    {"id": "ai-leader", "title": "AI leader",
     "description": "Understand how AI works, then use it well and lead its adoption in an engineering consultancy.",
     "packs": ["ai-general", "ai-use"]},
]
GRACE_DAYS = 7


def course_step(store: Store, course: dict[str, Any]) -> dict[str, Any]:
    row = store.one("SELECT COUNT(*) AS total, SUM(passed_at IS NOT NULL) AS passed FROM lessons WHERE course_id = ?", course["id"]) or {}
    total, passed = row.get("total") or 0, row.get("passed") or 0
    nxt = store.one("SELECT id, title FROM lessons WHERE course_id = ? AND passed_at IS NULL ORDER BY position LIMIT 1", course["id"])
    exam = bool(course.get("exam_passed_at"))
    return {"id": course["id"], "title": course["title"], "icon": course["icon"], "level": course["level"],
            "lessons": total, "passed": passed, "exam_passed": exam, "done": total > 0 and passed == total and exam,
            "next": ({"kind": "lesson", "id": nxt["id"], "title": nxt["title"], "url": f"/lesson/{nxt['id']}"} if nxt
                     else {"kind": "exam", "id": course["id"], "title": f"Final exam: {course['title']}", "url": f"/course/{course['id']}/exam"}
                     if total and not exam else None)}


def view(store: Store, path: dict[str, Any], today: str | None = None) -> dict[str, Any]:
    today_d = date.fromisoformat(today or local_day())
    courses = [c for c in (store.course(cid) for cid in path["course_ids"]) if c]
    steps = [course_step(store, c) for c in courses]
    units = sum(s["lessons"] + 1 for s in steps)
    done_units = sum(s["passed"] + (1 if s["exam_passed"] else 0) for s in steps)
    progress = done_units / units if units else 0
    finished = bool(steps) and all(s["done"] for s in steps)
    nxt = next((dict(s["next"], course_title=s["title"]) for s in steps if s["next"]), None)
    out: dict[str, Any] = {
        "id": path["id"], "title": path["title"], "description": path["description"], "pack": path["pack"],
        "target_date": path["target_date"], "created_at": path["created_at"], "courses": steps,
        "units": units, "done_units": done_units, "percent": round(100 * progress), "done": finished, "next": nxt,
        "status": "done" if finished else "no_date", "expected_percent": None, "days_left": None, "per_week": None,
    }
    if path["target_date"] and not finished:
        start = date.fromisoformat(path["created_at"][:10])
        target = date.fromisoformat(path["target_date"])
        span = max(1, (target - start).days)
        elapsed = min(span, max(0, (today_d - start).days - GRACE_DAYS))
        expected = elapsed / span
        days_left = (target - today_d).days
        remaining = units - done_units
        out.update(expected_percent=round(100 * expected), days_left=days_left,
                   per_week=math.ceil(remaining / max(1, days_left) * 7) if days_left > 0 else remaining,
                   status="overdue" if days_left < 0 else "on_track" if progress >= expected else "behind")
    return out


def all_paths(store: Store) -> list[dict[str, Any]]:
    return [view(store, p) for p in store.all("SELECT * FROM paths ORDER BY created_at")]


def get(store: Store, path_id: str) -> dict[str, Any] | None:
    row = store.one("SELECT * FROM paths WHERE id = ?", path_id)
    return view(store, row) if row else None


def _clean_courses(store: Store, course_ids: list[str]) -> list[str]:
    out: list[str] = []
    for cid in course_ids:
        if cid not in out and store.course(cid):
            out.append(cid)
    if not out:
        raise ValueError("Pick at least one course from your library.")
    return out


def _clean_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError("The target date should look like 2027-03-31.") from exc


def create(store: Store, title: str, description: str, course_ids: list[str], target_date: str | None, pack: str = "") -> dict[str, Any]:
    now = now_iso()
    path = {"id": new_id(), "title": title.strip()[:120], "description": description.strip()[:500],
            "course_ids": _clean_courses(store, course_ids), "target_date": _clean_date(target_date), "pack": pack,
            "created_at": now, "updated_at": now}
    store.insert("paths", path)
    store.log("path_created", title=path["title"], detail={"path_id": path["id"], "courses": len(path["course_ids"])})
    return view(store, path)


def update(store: Store, path_id: str, **fields: Any) -> dict[str, Any] | None:
    row = store.one("SELECT * FROM paths WHERE id = ?", path_id)
    if row is None:
        return None
    changes: dict[str, Any] = {}
    if fields.get("title") is not None:
        changes["title"] = fields["title"].strip()[:120]
    if fields.get("description") is not None:
        changes["description"] = fields["description"].strip()[:500]
    if fields.get("course_ids") is not None:
        changes["course_ids"] = _clean_courses(store, fields["course_ids"])
    if "target_date" in fields:
        changes["target_date"] = _clean_date(fields["target_date"])
    if changes:
        store.update("paths", path_id, **changes, updated_at=now_iso())
    return get(store, path_id)


def delete(store: Store, path_id: str) -> bool:
    return store.run("DELETE FROM paths WHERE id = ?", path_id) > 0


def active(store: Store) -> dict[str, Any] | None:
    """The path to show on Today: the first unfinished one, soonest target first."""
    open_paths = [p for p in all_paths(store) if not p["done"] and p["courses"]]
    open_paths.sort(key=lambda p: (p["target_date"] or "9999", p["created_at"]))
    return open_paths[0] if open_paths else None


def seed(store: Store) -> list[str]:
    added = []
    for built in BUILT_IN:
        key = f"path:{built['id']}"
        if store.setting(key):
            continue
        ids = []
        for pack in built["packs"]:
            row = store.one("SELECT id FROM courses WHERE pack = ? ORDER BY created_at LIMIT 1", pack)
            if row is None:
                break
            ids.append(row["id"])
        else:
            create(store, built["title"], built["description"], ids, None, pack=built["id"])
            store.set_setting(key, "1")
            added.append(built["id"])
    return added


def hub_view(store: Store) -> list[dict[str, Any]]:
    """For SirisOS: each unfinished path in a line or two."""
    out = []
    for p in all_paths(store):
        if p["done"]:
            continue
        out.append({"id": p["id"], "title": p["title"], "percent": p["percent"], "status": p["status"],
                    "target_date": p["target_date"], "days_left": p["days_left"], "per_week": p["per_week"],
                    "next": p["next"] and {"title": p["next"]["title"], "url": p["next"]["url"]}, "url": f"/path/{p['id']}"})
    return out


