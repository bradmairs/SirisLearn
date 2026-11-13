"""Builds courses in the background.

1. Creating a course stores it as `planning` and asks the model for a plan
   (sections and lessons). The course turns `ready` with every lesson
   `pending`, or `error` with the reason.
2. A lesson is written when it's first opened, and the one after it is
   written ahead so it's ready when you get there (SIRISLEARN_PREGENERATE=all
   writes the whole course straight after planning instead).
3. A time-sensitive lesson (regulations, products, fast-moving fields) can be
   refreshed once it's older than SIRISLEARN_REFRESH_DAYS (default 180): the
   writer gets the old version and, for AI courses, recent AI news, and
   rewrites it. Its review cards start over because the questions change.
4. Model output is checked before it's stored: a lesson keeps only
   well-formed questions, its diagrams are sanitised, and it needs at least
   six good questions or it fails and can be retried.

Work runs as asyncio tasks in the API process, at most two model calls at a
time, and a lesson is never written twice at once. Anything interrupted by a
restart is marked failed on startup so it can be retried.
"""

from __future__ import annotations

import asyncio
import logging
import math
import re
from datetime import datetime, timezone
from typing import Any

from app import config, photos, prompts, svg
from app.db import Store, get_store, new_id, now_iso
from app.llm import LLMError, get_llm

logger = logging.getLogger(__name__)

MIN_QUESTIONS = 6
MAX_POOL = 60
_tasks: dict[str, asyncio.Task] = {}
_semaphore: tuple[asyncio.AbstractEventLoop, asyncio.Semaphore] | None = None


def _limit() -> asyncio.Semaphore:
    global _semaphore
    loop = asyncio.get_running_loop()
    if _semaphore is None or _semaphore[0] is not loop:
        _semaphore = (loop, asyncio.Semaphore(2))
    return _semaphore[1]


def _spawn(key: str, coro_fn) -> None:
    task = _tasks.get(key)
    if task and not task.done():
        return
    _tasks[key] = asyncio.create_task(coro_fn())
    _tasks[key].add_done_callback(lambda _t, key=key: _tasks.pop(key, None))


def background(key: str, coro_fn) -> None:
    """Run one-off background work (at most one per key at a time)."""
    _spawn(key, coro_fn)


async def drain() -> None:
    """Tests: wait for every background job (and any they start) to finish."""
    while _tasks:
        await asyncio.gather(*list(_tasks.values()), return_exceptions=True)


def recover(store: Store) -> None:
    """On startup: nothing is running yet, so anything mid-flight was cut off."""
    store.run("UPDATE courses SET status = 'error', error = 'Interrupted by a restart. Retry to plan it again.' WHERE status = 'planning'")
    store.run("UPDATE lessons SET status = 'error', error = 'Interrupted by a restart. Retry to write it.' WHERE status = 'writing'")


# -- courses ---------------------------------------------------------------------


def create_course(topic: str, level: str, length: str, notes: str) -> dict[str, Any]:
    store = get_store()
    now = now_iso()
    course = {
        "id": new_id(), "topic": topic.strip(), "title": topic.strip(), "level": level, "length": length,
        "notes": notes.strip(), "status": "planning", "created_at": now, "updated_at": now,
    }
    store.insert("courses", course)
    store.log("course_created", title=course["title"], course=course)
    start_planning(course["id"])
    return store.course(course["id"])  # type: ignore[return-value]


def start_planning(course_id: str) -> None:
    get_store().update("courses", course_id, status="planning", error="", updated_at=now_iso())
    _spawn(f"plan:{course_id}", lambda: _plan(course_id))


async def _plan(course_id: str) -> None:
    store = get_store()
    course = store.course(course_id)
    if course is None:
        return
    llm = get_llm()
    try:
        if llm is None:
            raise LLMError("No model is set up. Add ANTHROPIC_API_KEY (or an Ollama model) to .env.")
        async with _limit():
            plan = await llm.json(
                system=prompts.PLANNER_SYSTEM, context="",
                prompt=prompts.outline_prompt(course["topic"], course["level"], course["length"], course["notes"]),
                schema=prompts.OUTLINE_SCHEMA, effort="medium", max_tokens=16000,
                meta={"purpose": "plan", "course_id": course_id},
            )
        sections = clean_outline(plan)
    except LLMError as exc:
        store.update("courses", course_id, status="error", error=str(exc), updated_at=now_iso())
        return
    except Exception:
        logger.exception("Planning %s failed", course_id)
        store.update("courses", course_id, status="error", error="Something went wrong planning this course. Retry.", updated_at=now_iso())
        return
    if store.course(course_id) is None:  # deleted while planning
        return
    store.update("courses", course_id, title=plan["title"].strip()[:120] or course["topic"],
                 summary=plan["summary"].strip(), icon=plan["icon"] if plan["icon"] in prompts.ICONS else "book",
                 sections=[{"title": s["title"], "summary": s["summary"]} for s in sections],
                 area=plan.get("area") if plan.get("area") in prompts.AREAS else "other", tags=clean_tags(plan.get("tags")),
                 status="ready", error="", updated_at=now_iso())
    rows, position = [], 0
    for s_idx, section in enumerate(sections):
        for lesson in section["lessons"]:
            rows.append({"id": new_id(), "course_id": course_id, "section_idx": s_idx, "position": position,
                         "title": lesson["title"], "summary": lesson["summary"], "status": "pending"})
            position += 1
    store.replace_lessons(course_id, rows)
    course = store.course(course_id)
    store.log("course_ready", title=course["title"], course=course, detail={"lessons": len(rows)})  # type: ignore[index]
    if config.pregenerate() == "all":
        for row in rows:
            ensure_lesson(row["id"])
    elif rows:
        ensure_lesson(rows[0]["id"])


def clean_tags(tags: Any) -> list[str]:
    out: list[str] = []
    for tag in tags or []:
        tag = re.sub(r"[^a-z0-9+#. -]", "", str(tag).lower()).strip().replace(" ", "-")[:32]
        if tag and tag not in out:
            out.append(tag)
    return out[:8]


def clean_outline(plan: dict[str, Any]) -> list[dict[str, Any]]:
    sections = []
    for section in plan.get("sections") or []:
        lessons = [
            {"title": str(l.get("title") or "").strip()[:160], "summary": str(l.get("summary") or "").strip()}
            for l in section.get("lessons") or []
            if str(l.get("title") or "").strip()
        ][:8]
        if lessons and str(section.get("title") or "").strip():
            sections.append({"title": section["title"].strip()[:160], "summary": str(section.get("summary") or "").strip(), "lessons": lessons})
    if not sections:
        raise LLMError("The model didn't return a usable course plan. Retry.")
    return sections[:10]


def retry_course(course_id: str) -> None:
    store = get_store()
    course = store.course(course_id)
    if course is None:
        return
    if course["status"] == "error":
        start_planning(course_id)
        return
    for lesson in store.lessons(course_id):
        if lesson["status"] == "error":
            ensure_lesson(lesson["id"])


# -- lessons ---------------------------------------------------------------------


def ensure_lesson(lesson_id: str, regenerate: bool = False, refresh: bool = False) -> None:
    """Start writing a lesson if it isn't written (or being written) yet.
    `refresh` rewrites a written lesson from its old version."""
    store = get_store()
    lesson = store.lesson(lesson_id)
    if lesson is None or (lesson["status"] in ("ready", "writing") and not (regenerate or refresh)):
        return
    if f"lesson:{lesson_id}" in _tasks:
        return
    previous = lesson if refresh and lesson["status"] == "ready" and lesson.get("content") else None
    store.update("lessons", lesson_id, status="writing", error="")
    _spawn(f"lesson:{lesson_id}", lambda: _write(lesson_id, previous))


def refresh_days() -> int:
    return max(1, int(config.env("SIRISLEARN_REFRESH_DAYS", "180")))


def stale(lesson: dict[str, Any], now: datetime | None = None) -> dict[str, Any] | None:
    """When a time-sensitive lesson is due a refresh: its age, else None."""
    content = lesson.get("content") or {}
    if lesson.get("status") != "ready" or not content.get("time_sensitive") or not lesson.get("generated_at"):
        return None
    age = ((now or datetime.now(timezone.utc)) - datetime.fromisoformat(lesson["generated_at"])).days
    return {"written": lesson["generated_at"], "days": age} if age >= refresh_days() else None


def is_ai_course(course: dict[str, Any]) -> bool:
    tags = set(course.get("tags") or [])
    return bool(tags & {"ai", "artificial-intelligence", "llms", "machine-learning", "generative-ai"}) or (course.get("pack") or "").startswith("ai-")


def prefetch_after(lesson: dict[str, Any]) -> None:
    following = get_store().one(
        "SELECT id FROM lessons WHERE course_id = ? AND position > ? AND status IN ('pending', 'error') ORDER BY position LIMIT 1",
        lesson["course_id"], lesson["position"],
    )
    if following:
        ensure_lesson(following["id"])


async def _write(lesson_id: str, previous: dict[str, Any] | None = None) -> None:
    from app import news

    store = get_store()
    lesson = store.lesson(lesson_id)
    course = store.course(lesson["course_id"]) if lesson else None
    if lesson is None or course is None:
        return
    llm = get_llm()
    try:
        if llm is None:
            raise LLMError("No model is set up. Add ANTHROPIC_API_KEY (or an Ollama model) to .env.")
        sections = _plan_with_lessons(store, course)
        section = sections[lesson["section_idx"]]
        lesson_number = next(i for i, l in enumerate(section["lessons"], 1) if l["id"] == lesson_id)
        if previous:
            items = await news.recent(days=refresh_days()) if is_ai_course(course) else []
            prompt = prompts.refresh_prompt(lesson["section_idx"] + 1, lesson_number, section["title"], previous,
                                            previous.get("generated_at") or "", news.as_prompt(items[:25]) if items else "")
        else:
            prompt = prompts.lesson_prompt(lesson["section_idx"] + 1, lesson_number, section["title"], lesson["title"], lesson["summary"])
        async with _limit():
            raw = await llm.json(
                system=prompts.WRITER_SYSTEM,
                context=prompts.course_context(course, sections),
                prompt=prompt,
                schema=prompts.LESSON_SCHEMA, effort=config.env("SIRISLEARN_EFFORT", "medium"), max_tokens=64000,
                meta={"purpose": "refresh" if previous else "lesson", "course_id": course["id"], "lesson_id": lesson_id},
            )
        content = clean_lesson(raw)
        if previous:
            content["refreshed_at"] = now_iso()
        if content.get("photo_query"):
            content["photo"] = await photos.find(content["photo_query"])
    except LLMError as exc:
        if previous:  # keep the old version readable
            store.update("lessons", lesson_id, status="ready", error=f"Refreshing failed: {exc}")
        else:
            store.update("lessons", lesson_id, status="error", error=str(exc))
        return
    except Exception:
        logger.exception("Writing lesson %s failed", lesson_id)
        if previous:
            store.update("lessons", lesson_id, status="ready", error="Refreshing failed. Try again later.")
        else:
            store.update("lessons", lesson_id, status="error", error="Something went wrong writing this lesson. Retry.")
        return
    if store.lesson(lesson_id) is None:
        return
    store.update("lessons", lesson_id, status="ready", error="", content=content, generated_at=now_iso())
    if previous:
        store.run("DELETE FROM reviews WHERE lesson_id = ?", lesson_id)  # its questions are new
        store.log("lesson_refreshed", title=lesson["title"], course=course, lesson_id=lesson_id)


def _plan_with_lessons(store: Store, course: dict[str, Any]) -> list[dict[str, Any]]:
    sections = [dict(s, lessons=[]) for s in course["sections"]]
    for lesson in store.lessons(course["id"]):
        sections[lesson["section_idx"]]["lessons"].append(lesson)
    return sections


def clean_lesson(raw: dict[str, Any], max_questions: int | None = prompts.QUESTIONS_PER_LESSON) -> dict[str, Any]:
    """Check and tidy a written lesson. Course packs pass max_questions=None
    to keep a bigger question pool."""
    questions = clean_questions(raw.get("questions") or [], 1)[:max_questions]
    body = str(raw.get("body") or "").strip()
    if len(body) < 200 or len(questions) < MIN_QUESTIONS:
        raise LLMError("The lesson came back incomplete. Retry to write it again.")
    figure = svg.sanitize(raw.get("figure_svg"))
    out = {
        "body": body,
        "minutes": max(2, min(30, int(raw.get("minutes") or 8))),
        "key_points": [str(p).strip() for p in raw.get("key_points") or [] if str(p).strip()][:6],
        "figure_svg": figure,
        "figure_caption": str(raw.get("figure_caption") or "").strip() if figure else "",
        "questions": questions,
        "photo_query": str(raw.get("photo_query") or "").strip()[:80],
        "time_sensitive": raw.get("time_sensitive") is True,
    }
    return out


def clean_questions(raw: list[Any], start: int) -> list[dict[str, Any]]:
    """Clean a batch of questions and number them from q<start>."""
    out = []
    for q in raw or []:
        cleaned = clean_question(q)
        if cleaned:
            cleaned["id"] = f"q{start + len(out)}"
            out.append(cleaned)
    return out


# -- fresh questions and photos -------------------------------------------------


def extend_questions(lesson_id: str) -> None:
    """Write 10 new questions for a lesson in the background, so the next
    retake has questions you haven't seen. Does nothing without a model."""
    if get_llm() is None or f"questions:{lesson_id}" in _tasks:
        return
    _spawn(f"questions:{lesson_id}", lambda: _extend(lesson_id))


async def _extend(lesson_id: str) -> None:
    store = get_store()
    lesson = store.lesson(lesson_id)
    llm = get_llm()
    if lesson is None or lesson["status"] != "ready" or llm is None:
        return
    if len(lesson["content"]["questions"]) >= MAX_POOL:
        return
    try:
        async with _limit():
            raw = await llm.json(system=prompts.QUESTION_WRITER_SYSTEM, context="", prompt=prompts.questions_prompt(lesson),
                                 schema=prompts.QUESTIONS_SCHEMA, effort=config.env("SIRISLEARN_EFFORT", "medium"), max_tokens=32000,
                                 meta={"purpose": "questions", "course_id": lesson["course_id"], "lesson_id": lesson_id})
    except LLMError:
        logger.warning("Writing fresh questions for %s failed", lesson_id, exc_info=True)
        return
    current = store.lesson(lesson_id)
    if current is None or current["status"] != "ready":
        return
    pool = current["content"]["questions"]
    numbers = [int(q["id"][1:]) for q in pool if q["id"][1:].isdigit()]
    fresh = clean_questions(raw.get("questions") or [], max(numbers, default=0) + 1)
    if fresh:
        store.update("lessons", lesson_id, content={**current["content"], "questions": pool + fresh})


def ensure_photo(lesson: dict[str, Any]) -> None:
    """Find a lesson's photo once (lessons from a course pack, or written
    before photos existed)."""
    content = lesson.get("content") or {}
    if content.get("photo_query") and "photo" not in content and photos.enabled():
        _spawn(f"photo:{lesson['id']}", lambda: _photo(lesson["id"]))


async def _photo(lesson_id: str) -> None:
    found = await photos.find((get_store().lesson(lesson_id) or {}).get("content", {}).get("photo_query", ""))
    current = get_store().lesson(lesson_id)
    if current and current["content"] is not None:
        get_store().update("lessons", lesson_id, content={**current["content"], "photo": found})


def clean_question(q: dict[str, Any]) -> dict[str, Any] | None:
    prompt = str(q.get("prompt") or "").strip()
    kind = q.get("kind")
    if not prompt or kind not in prompts.QUESTION_KINDS:
        return None
    image = svg.sanitize(q.get("svg"))
    out: dict[str, Any] = {
        "kind": kind,
        "prompt": prompt,
        "svg": image,
        "image_alt": str(q.get("image_alt") or "").strip() if image else "",
        "explanation": str(q.get("explanation") or "").strip(),
    }
    if kind == "mcq":
        options = [str(o).strip() for o in q.get("options") or []]
        answer = q.get("answer_index")
        options = options[:6]
        if len(options) < 2 or not all(options) or not isinstance(answer, int) or not 0 <= answer < len(options):
            return None
        out.update(options=options, answer_index=answer)
    elif kind == "calc":
        value = q.get("answer_value")
        working = str(q.get("working") or "").strip()
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not working:
            return None
        tolerance = q.get("tolerance")
        tolerance = float(tolerance) if isinstance(tolerance, (int, float)) and not isinstance(tolerance, bool) and math.isfinite(tolerance) else 2.0
        out.update(answer_value=float(value), tolerance=min(10.0, max(0.5, tolerance)),
                   unit=str(q.get("unit") or "").strip()[:20], working=working)
    else:
        key_points = [str(p).strip() for p in q.get("key_points") or [] if str(p).strip()]
        model_answer = str(q.get("model_answer") or "").strip()
        if not model_answer:
            return None
        out.update(model_answer=model_answer, key_points=key_points[:5])
    return out
