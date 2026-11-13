"""What SirisOS reads (its SirisLearn connector, SirisOS ADR 112).

All three routes need `X-API-Key: <SIRISLEARN_HUB_KEY>`. Links are paths in
this app ("/lesson/abc"); SirisOS puts SIRISLEARN_PUBLIC_URL in front.

- /status: up, version, and whether a model is set up.
- /summary: the widget numbers (streak, XP against the daily goal, level,
  courses) and what to do next. `streak.at_risk` drives the SirisOS inbox
  item "your streak ends at midnight". `paths` (1.4) lists unfinished
  learning paths with percent, status (on_track, behind, overdue, no_date)
  and the next step; a "behind" path is a SirisOS inbox item.
- /search: courses and lessons by title, topic and summary.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from app import llm, paths, progress
from app.auth import require_hub_key
from app.db import get_store
from app.version import VERSION

router = APIRouter(prefix="/api/hub/v1", tags=["sirisos"], dependencies=[Depends(require_hub_key)])


@router.get("/status")
def status() -> dict[str, Any]:
    return {"status": "ok", "version": VERSION, "llm": llm.describe()}


@router.get("/summary")
def summary() -> dict[str, Any]:
    data = progress.summary(get_store())
    nxt = data["continue"]
    data["continue"] = nxt and {**nxt, "url": f"/lesson/{nxt['lesson_id']}"}
    data.pop("path", None)
    data.pop("weak_spot", None)
    data["paths"] = paths.hub_view(get_store())
    recent = get_store().events(kinds=["quiz_finished", "course_completed", "achievement"], limit=5)
    data["recent"] = [
        {"kind": e["kind"], "title": e["title"], "course_title": e["course_title"], "xp": e["xp"], "ts": e["ts"],
         "url": f"/lesson/{e['lesson_id']}" if e["lesson_id"] else "/awards" if e["kind"] == "achievement" else None}
        for e in recent
    ]
    return data


@router.get("/search")
def search(q: str = Query("", max_length=200)) -> dict[str, Any]:
    words = [w for w in q.lower().split() if w]
    if not words:
        return {"hits": []}
    store = get_store()
    hits: list[dict[str, Any]] = []

    def matches(*texts: Any) -> bool:
        hay = " ".join(str(t) for t in texts if t).lower()
        return all(w in hay for w in words)

    for course in store.courses():
        if matches(course["title"], course["topic"], course["summary"]):
            p = progress.course_progress(store, course["id"])
            hits.append({"title": course["title"], "subtitle": f"Course · {p['passed']}/{p['lessons']} lessons",
                         "url": f"/course/{course['id']}", "kind": "course"})
    for lesson in store.all("SELECT l.id, l.title, l.summary, l.passed_at, c.title AS course_title FROM lessons l"
                            " JOIN courses c ON c.id = l.course_id ORDER BY l.position"):
        if matches(lesson["title"], lesson["summary"]):
            hits.append({"title": lesson["title"], "subtitle": f"Lesson · {lesson['course_title']}" + (" · passed" if lesson["passed_at"] else ""),
                         "url": f"/lesson/{lesson['id']}", "kind": "lesson"})
    return {"hits": hits[:20]}
