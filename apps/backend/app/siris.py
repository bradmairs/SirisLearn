"""SirisLearn's links to the rest of Siris.

- **Second Brain** (through SirisAI, SIRISAI_URL + SIRISAI_API_KEY): when you
  first pass a lesson, its key points are captured into the brain
  (`POST /siris/brain/capture`), where Siris files and links them like any
  other note. Turn it off in Settings.
- **Topic suggestions**: the brain's most active topics
  (`GET /siris/brain/insights`) become "learn about this" ideas on Today,
  skipping anything you already have a course on.
- **Ask Siris**: SIRISOS_PUBLIC_URL makes "Continue in Siris" open the SirisOS
  assistant with your question (`/assistant?q=`).
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app import config
from app.db import Store, get_store, now_iso

logger = logging.getLogger(__name__)

# Tests swap this for an httpx.MockTransport.
transport: httpx.AsyncBaseTransport | None = None

DEFAULT_IDEAS = [
    "How black holes form", "Personal finance basics", "Stoic philosophy", "Machine learning fundamentals",
    "Home networking", "Wine tasting", "The history of Rome", "Negotiation skills",
]


def sirisai_url() -> str:
    return config.env("SIRISAI_URL").rstrip("/")


def brain_configured() -> bool:
    return bool(sirisai_url() and config.env("SIRISAI_API_KEY"))


def sirisos_url() -> str:
    return config.env("SIRISOS_PUBLIC_URL").rstrip("/")


def _headers() -> dict[str, str]:
    out = {"Authorization": f"Bearer {config.env('SIRISAI_API_KEY')}", "X-Siris-Client": "SirisLearn"}
    if config.env("SIRISAI_USER"):
        out["X-Siris-User"] = config.env("SIRISAI_USER")
    return out


def brain_enabled(store: Store) -> bool:
    return brain_configured() and store.setting("brain_capture", "on") == "on"


def lesson_note(lesson: dict[str, Any], course: dict[str, Any]) -> str:
    points = "\n".join(f"- {p}" for p in lesson["content"].get("key_points") or [])
    return (f"{lesson['title']}\n\nWhat I learned in the SirisLearn course \"{course['title']}\" "
            f"({course['level']}), lesson: {lesson['title']}.\n\n{lesson.get('summary') or ''}\n\nKey points:\n{points}")


async def save_lesson(lesson_id: str) -> bool:
    """Capture a passed lesson's key points into the Second Brain, once."""
    store = get_store()
    lesson = store.lesson(lesson_id)
    course = store.course(lesson["course_id"]) if lesson else None
    if not lesson or not course or lesson.get("brain_saved_at") or not brain_enabled(store):
        return False
    public = config.env("SIRISLEARN_PUBLIC_URL").rstrip("/")
    body = {
        "text": lesson_note(lesson, course),
        "url": f"{public}/lesson/{lesson_id}" if public else "",
        "tags": ["sirislearn", "learning", *(course.get("tags") or [])[:4]],
    }
    try:
        async with httpx.AsyncClient(timeout=60.0, transport=transport) as client:
            response = await client.post(f"{sirisai_url()}/siris/brain/capture", json=body, headers=_headers())
            response.raise_for_status()
    except httpx.HTTPError:
        logger.warning("Saving lesson %s to the Second Brain failed", lesson_id, exc_info=True)
        return False
    store.update("lessons", lesson_id, brain_saved_at=now_iso())
    store.log("brain_saved", title=lesson["title"], course=course, lesson_id=lesson_id)
    return True


async def suggestions(store: Store, limit: int = 6) -> dict[str, Any]:
    """Topic ideas: from the Second Brain's busiest topics when it's linked."""
    have = " ".join(f"{c['topic']} {c['title']} {' '.join(c.get('tags') or [])}".lower() for c in store.courses())
    ideas: list[str] = []
    source = "ideas"
    if brain_configured():
        try:
            async with httpx.AsyncClient(timeout=8.0, transport=transport) as client:
                response = await client.get(f"{sirisai_url()}/siris/brain/insights", params={"days": 30}, headers=_headers())
                response.raise_for_status()
                topics = response.json().get("topics") or []
            for t in sorted(topics, key=lambda t: -(t.get("notes") or 0)):
                tag = str(t.get("tag") or "").strip()
                name = tag.replace("-", " ").replace("_", " ").strip()
                if name and name.lower() not in have and tag.lower() not in ("sirislearn", "learning", "inbox"):
                    ideas.append(name[:1].upper() + name[1:])
            source = "brain" if ideas else source
        except (httpx.HTTPError, ValueError, AttributeError):
            logger.info("Second Brain insights unavailable", exc_info=True)
    if not ideas:
        ideas = [i for i in DEFAULT_IDEAS if i.lower() not in have]
    return {"source": source, "ideas": ideas[:limit]}
