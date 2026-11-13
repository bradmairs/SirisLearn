"""What's new in AI: a lesson each month, written from recent AI news
(app/news.py) into a living course, "What's new in AI", with a section per
year. It needs a model and at least a few news items.

The background jobs (app/jobs.py) make the month's lesson from
SIRISLEARN_AI_UPDATE_DAY (default the 1st), trying at most once a day until
it works. It can be made straight away from Settings, and turned off there
(or for good with SIRISLEARN_AI_UPDATES=false).
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from app import config, news, prompts
from app.db import Store, local_day, new_id, now_iso
from app.generator import background, clean_lesson
from app.llm import LLMError, get_llm

logger = logging.getLogger(__name__)

PACK = "ai-updates"
MIN_ITEMS = 3


def allowed() -> bool:
    return config.env("SIRISLEARN_AI_UPDATES", "true").lower() not in ("0", "false", "no")


def enabled(store: Store) -> bool:
    return allowed() and store.setting("ai_updates", "on") == "on"


def update_day() -> int:
    return min(28, max(1, int(config.env("SIRISLEARN_AI_UPDATE_DAY", "1"))))


def month_label(month: str) -> str:
    return date.fromisoformat(f"{month}-01").strftime("%B %Y")


def course(store: Store) -> dict[str, Any] | None:
    return store.one("SELECT * FROM courses WHERE pack = ? ORDER BY created_at LIMIT 1", PACK)


def _ensure_course(store: Store) -> dict[str, Any]:
    existing = course(store)
    if existing:
        return existing
    now = now_iso()
    course_id = new_id()
    store.insert("courses", {
        "id": course_id, "topic": "What's new in AI", "title": "What's new in AI",
        "summary": "A lesson each month on the AI developments that matter for professional and engineering work, written from recent news with its sources.",
        "icon": "lightbulb", "level": "intermediate", "length": "standard",
        "area": "technology", "tags": ["ai", "ai-news", "ai-literacy"], "sections": [], "pack": PACK,
        "notes": "Monthly news round-up for a professional engineer who wants to stay one of the AI leaders at their consultancy.",
        "status": "ready", "created_at": now, "updated_at": now,
    })
    return store.course(course_id)  # type: ignore[return-value]


def status(store: Store) -> dict[str, Any]:
    c = course(store)
    last = store.one("SELECT title, generated_at FROM lessons WHERE course_id = ? ORDER BY position DESC LIMIT 1", c["id"]) if c else None
    return {"allowed": allowed(), "enabled": enabled(store), "course_id": c["id"] if c else None,
            "last": last, "error": store.setting("ai_update_error") or None, "feeds": len(news.feeds()),
            "model": get_llm() is not None, "running": store.setting("ai_update_running") == "yes"}


def due(store: Store, today: str) -> bool:
    month = today[:7]
    return (enabled(store) and get_llm() is not None and int(today[8:10]) >= update_day()
            and store.setting("ai_update_month") != month and store.setting("ai_update_tried") != today)


async def make(store: Store, month: str) -> str:
    """Write the month's lesson; returns its id. Raises LLMError when it can't."""
    llm = get_llm()
    if llm is None:
        raise LLMError("No model is set up, so the monthly AI update can't be written.")
    label = month_label(month)
    title = f"What's new in AI: {label}"
    c = _ensure_course(store)
    found = store.one("SELECT id FROM lessons WHERE course_id = ? AND title = ?", c["id"], title)
    if found:
        return found["id"]
    items = await news.recent()
    if len(items) < MIN_ITEMS:
        raise LLMError(f"Only {len(items)} recent news item{'s' if len(items) != 1 else ''} could be read from the AI feeds, too few for an update.")
    raw = await llm.json(system=prompts.UPDATE_SYSTEM, context="", prompt=prompts.update_prompt(label, news.as_prompt(items)),
                         schema=prompts.LESSON_SCHEMA, effort=config.env("SIRISLEARN_EFFORT", "medium"), max_tokens=64000,
                         meta={"purpose": "ai-update", "course_id": c["id"]})
    content = {**clean_lesson(raw), "time_sensitive": False, "photo_query": "", "sources": len(items)}
    c = store.course(c["id"]) or c
    sections = list(c["sections"] or [])
    year = month[:4]
    section_idx = next((i for i, s in enumerate(sections) if s["title"] == year), None)
    if section_idx is None:
        sections.append({"title": year, "summary": f"Monthly AI updates in {year}."})
        section_idx = len(sections) - 1
    position = (store.one("SELECT MAX(position) AS p FROM lessons WHERE course_id = ?", c["id"]) or {}).get("p")
    lesson_id = new_id()
    store.insert("lessons", {"id": lesson_id, "course_id": c["id"], "section_idx": section_idx,
                             "position": 0 if position is None else position + 1, "title": title,
                             "summary": f"The AI developments that mattered in {label}, and what they mean for your work.",
                             "status": "ready", "content": content, "generated_at": now_iso()})
    store.update("courses", c["id"], sections=sections, completed_at=None, updated_at=now_iso())
    store.log("ai_update", title=title, course=c, lesson_id=lesson_id, detail={"items": len(items)})
    return lesson_id


async def run(store: Store, month: str | None = None) -> str | None:
    """make(), recording the outcome for Settings; never raises."""
    month = month or local_day()[:7]
    store.set_setting("ai_update_running", "yes")
    try:
        lesson_id = await make(store, month)
    except LLMError as exc:
        store.set_setting("ai_update_error", str(exc))
        return None
    except Exception:
        logger.exception("The monthly AI update failed")
        store.set_setting("ai_update_error", "Something went wrong writing the monthly AI update.")
        return None
    finally:
        store.set_setting("ai_update_running", "no")
    store.set_setting("ai_update_month", month)
    store.set_setting("ai_update_error", "")
    return lesson_id


def start(store: Store) -> None:
    """Make this month's update in the background."""
    background("ai-update", lambda: run(store))
