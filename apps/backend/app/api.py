"""The web app's API: courses, lessons, quizzes, the daily review, final
exams and certificates, progress, history, achievements, the tutor and
settings. Every route needs the signed-in user."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, Field

from app import achievements, generator, llm, progress, prompts, quiz, siris, spaced
from app.auth import require_user
from app.db import get_store, local_day, now_iso

router = APIRouter(prefix="/api", dependencies=[Depends(require_user)])


class NewCourse(BaseModel):
    topic: str = Field(min_length=2, max_length=300)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    length: Literal["short", "standard", "deep"] = "standard"
    notes: str = Field("", max_length=2000)


class CoursePatch(BaseModel):
    archived: bool | None = None


class Answer(BaseModel):
    question_id: str
    choice: int | None = None
    text: str | None = Field(None, max_length=4000)


class Ask(BaseModel):
    question: str = Field(min_length=2, max_length=2000)


class Settings(BaseModel):
    daily_goal: int | None = Field(None, ge=10, le=1000)
    brain_capture: bool | None = None


def _course_or_404(course_id: str) -> dict[str, Any]:
    course = get_store().course(course_id)
    if course is None:
        raise HTTPException(404, "No such course.")
    return course


def _lesson_or_404(lesson_id: str) -> dict[str, Any]:
    lesson = get_store().lesson(lesson_id)
    if lesson is None:
        raise HTTPException(404, "No such lesson.")
    return lesson


def _course_card(course: dict[str, Any]) -> dict[str, Any]:
    store = get_store()
    nxt = progress.next_lesson(store, course["id"])
    return {
        **{k: course[k] for k in ("id", "topic", "title", "summary", "icon", "level", "length", "status", "error",
                                  "created_at", "updated_at", "completed_at", "area", "tags", "pack", "exam_best", "exam_passed_at")},
        "archived": bool(course["archived"]),
        "progress": progress.course_progress(store, course["id"]),
        "next_lesson": nxt,
    }


def _lesson_summary(lesson: dict[str, Any]) -> dict[str, Any]:
    return {k: lesson[k] for k in ("id", "title", "summary", "status", "error", "best_score", "passed_at", "read_at", "position")}


# -- home ----------------------------------------------------------------------


@router.get("/summary")
def summary() -> dict[str, Any]:
    return progress.summary(get_store())


@router.get("/suggestions")
async def suggestions() -> dict[str, Any]:
    return await siris.suggestions(get_store())


# -- courses -------------------------------------------------------------------


@router.get("/courses")
def list_courses() -> list[dict[str, Any]]:
    return [_course_card(c) for c in get_store().courses()]


@router.post("/courses", status_code=201)
async def create_course(body: NewCourse) -> dict[str, Any]:
    return _course_card(generator.create_course(body.topic, body.level, body.length, body.notes))


@router.get("/courses/{course_id}")
def get_course(course_id: str) -> dict[str, Any]:
    store = get_store()
    course = _course_or_404(course_id)
    lessons = store.lessons(course_id)
    sections = [
        {**s, "lessons": [_lesson_summary(l) for l in lessons if l["section_idx"] == i]}
        for i, s in enumerate(course["sections"])
    ]
    tags = set(course.get("tags") or [])
    related = []
    for other in store.courses():
        if other["id"] == course_id or other["status"] != "ready":
            continue
        shared = len(tags & set(other.get("tags") or [])) + (1 if other["area"] and other["area"] == course["area"] else 0)
        if shared:
            related.append((shared, other))
    related.sort(key=lambda r: -r[0])
    return {**_course_card(course), "notes": course["notes"], "sections": sections,
            "related": [{k: o[k] for k in ("id", "title", "icon", "level")} for _, o in related[:4]],
            "exam": _exam_status(course)}


@router.patch("/courses/{course_id}")
def patch_course(course_id: str, body: CoursePatch) -> dict[str, Any]:
    _course_or_404(course_id)
    if body.archived is not None:
        get_store().update("courses", course_id, archived=int(body.archived), updated_at=now_iso())
    return _course_card(get_store().course(course_id))  # type: ignore[arg-type]


@router.post("/courses/{course_id}/retry")
async def retry_course(course_id: str) -> dict[str, Any]:
    _course_or_404(course_id)
    generator.retry_course(course_id)
    return _course_card(get_store().course(course_id))  # type: ignore[arg-type]


@router.delete("/courses/{course_id}", status_code=204, response_class=Response)
def delete_course(course_id: str) -> Response:
    _course_or_404(course_id)
    get_store().delete_course(course_id)
    return Response(status_code=204)


# -- final exam and certificate ---------------------------------------------------


def _exam_status(course: dict[str, Any]) -> dict[str, Any]:
    p = progress.course_progress(get_store(), course["id"])
    unlocked = bool(p["lessons"]) and p["passed"] == p["lessons"]
    return {"unlocked": unlocked, "questions": min(quiz.EXAM_SIZE, p["lessons"] * 10), "pass_mark": progress.EXAM_PASS_MARK,
            "best": course.get("exam_best"), "passed_at": course.get("exam_passed_at"),
            "lessons_left": p["lessons"] - p["passed"]}


@router.post("/courses/{course_id}/exam", status_code=201)
def start_exam(course_id: str) -> dict[str, Any]:
    course = _course_or_404(course_id)
    if not _exam_status(course)["unlocked"]:
        raise HTTPException(409, "Pass every lesson first to unlock the final exam.")
    return quiz.start_exam(get_store(), course)


@router.get("/courses/{course_id}/certificate")
def certificate(course_id: str, user: str = Depends(require_user)) -> dict[str, Any]:
    store = get_store()
    course = _course_or_404(course_id)
    if not course.get("exam_passed_at"):
        raise HTTPException(404, "Pass the final exam to earn this certificate.")
    p = progress.course_progress(store, course_id)
    minutes = sum(int((l.get("content") or {}).get("minutes") or 0) for l in store.lessons(course_id))
    return {"name": user[:1].upper() + user[1:], "course": course["title"], "level": course["level"], "summary": course["summary"],
            "issued": course["exam_passed_at"], "score": course.get("exam_best"), "lessons": p["lessons"], "minutes": minutes,
            "sections": [s["title"] for s in course["sections"]],
            "reference": f"SL-{course_id[:6].upper()}-{course['exam_passed_at'][:10].replace('-', '')}"}


# -- lessons -------------------------------------------------------------------


@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str) -> dict[str, Any]:
    store = get_store()
    lesson = _lesson_or_404(lesson_id)
    course = store.course(lesson["course_id"])
    if lesson["status"] == "pending":
        generator.ensure_lesson(lesson_id)
        lesson = store.lesson(lesson_id)
    content = None
    if lesson["status"] == "ready":
        if not lesson["read_at"]:
            store.update("lessons", lesson_id, read_at=now_iso())
            store.log("lesson_read", title=lesson["title"], course=course, lesson_id=lesson_id)
            store.touch_course(lesson["course_id"])
        generator.prefetch_after(lesson)
        generator.ensure_photo(lesson)
        content = {k: v for k, v in lesson["content"].items() if k != "questions"}
        content["question_count"] = min(quiz.QUIZ_SIZE, len(lesson["content"]["questions"]))
        content["pool_size"] = len(lesson["content"]["questions"])
        content["unseen"] = quiz.unseen_count(store, lesson)
    siblings = store.lessons(lesson["course_id"])
    index = next(i for i, l in enumerate(siblings) if l["id"] == lesson_id)
    return {
        **_lesson_summary(lesson),
        "course": {"id": course["id"], "title": course["title"], "icon": course["icon"], "level": course["level"]},
        "section": course["sections"][lesson["section_idx"]]["title"] if course["sections"] else "",
        "number": index + 1,
        "of": len(siblings),
        "previous_id": siblings[index - 1]["id"] if index > 0 else None,
        "next_id": siblings[index + 1]["id"] if index + 1 < len(siblings) else None,
        "brain_saved_at": lesson.get("brain_saved_at"),
        "content": content,
    }


@router.post("/lessons/{lesson_id}/regenerate")
async def regenerate_lesson(lesson_id: str) -> dict[str, Any]:
    lesson = _lesson_or_404(lesson_id)
    if lesson["status"] == "writing":
        raise HTTPException(409, "This lesson is already being written.")
    generator.ensure_lesson(lesson_id, regenerate=True)
    return _lesson_summary(get_store().lesson(lesson_id))  # type: ignore[arg-type]


@router.post("/lessons/{lesson_id}/attempts", status_code=201)
async def start_quiz(lesson_id: str) -> dict[str, Any]:
    store = get_store()
    lesson = _lesson_or_404(lesson_id)
    if lesson["status"] != "ready":
        raise HTTPException(409, "This lesson isn't written yet.")
    started = quiz.start_lesson(store, lesson)
    if quiz.unseen_count(store, store.lesson(lesson_id)) < quiz.QUIZ_SIZE:  # type: ignore[arg-type]
        generator.extend_questions(lesson_id)  # so the next retake is fresh
    return started


@router.get("/lessons/{lesson_id}/attempts")
def lesson_attempts(lesson_id: str) -> list[dict[str, Any]]:
    _lesson_or_404(lesson_id)
    return get_store().all(
        "SELECT id, started_at, finished_at, correct, total, score, xp FROM attempts"
        " WHERE lesson_id = ? AND kind = 'lesson' AND finished_at IS NOT NULL ORDER BY finished_at DESC", lesson_id)


@router.post("/lessons/{lesson_id}/ask")
async def ask(lesson_id: str, body: Ask) -> dict[str, Any]:
    """Ask Siris about the lesson (a one-off explanation from the tutor)."""
    store = get_store()
    lesson = _lesson_or_404(lesson_id)
    if lesson["status"] != "ready":
        raise HTTPException(409, "This lesson isn't written yet.")
    model = llm.get_llm()
    handoff = f"{siris.sirisos_url()}/assistant" if siris.sirisos_url() else None
    if model is None:
        raise HTTPException(503, "No model is set up, so Siris can't answer here. Add ANTHROPIC_API_KEY to .env.")
    course = store.course(lesson["course_id"])
    try:
        out = await model.json(system=prompts.TUTOR_SYSTEM, context=prompts.lesson_context(lesson, course),  # type: ignore[arg-type]
                               prompt=prompts.tutor_prompt(body.question), schema=prompts.TUTOR_SCHEMA, effort="low",
                               max_tokens=8000, meta={"purpose": "tutor", "course_id": lesson["course_id"], "lesson_id": lesson_id})
    except llm.LLMError as exc:
        raise HTTPException(502, str(exc)) from exc
    return {"answer": str(out.get("answer") or "").strip(), "sirisos_assistant": handoff}


# -- quizzes: lesson, review and exam --------------------------------------------


def _attempt_or_404(attempt_id: str) -> dict[str, Any]:
    attempt = get_store().attempt(attempt_id)
    if attempt is None:
        raise HTTPException(404, "No such quiz.")
    return attempt


@router.post("/attempts/{attempt_id}/answer")
async def answer(attempt_id: str, body: Answer) -> dict[str, Any]:
    attempt = _attempt_or_404(attempt_id)
    if attempt["finished_at"]:
        raise HTTPException(409, "This quiz is already finished.")
    if body.question_id in attempt["answers"]:
        raise HTTPException(409, "You've already answered this question.")
    try:
        return await quiz.answer(get_store(), attempt, body.question_id, body.choice, body.text)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.post("/attempts/{attempt_id}/finish")
async def finish(attempt_id: str) -> dict[str, Any]:
    store = get_store()
    attempt = _attempt_or_404(attempt_id)
    if attempt["finished_at"]:
        raise HTTPException(409, "This quiz is already finished.")
    result = quiz.finish(store, attempt)
    if attempt["kind"] == "lesson":
        lesson = store.lesson(attempt["lesson_id"])
        if lesson and quiz.unseen_count(store, lesson) < quiz.QUIZ_SIZE:
            generator.extend_questions(lesson["id"])
        if result.get("first_pass") and siris.brain_enabled(store):
            generator.background(f"brain:{attempt['lesson_id']}", lambda: siris.save_lesson(attempt["lesson_id"]))
            result["brain"] = "saving"
    return result


@router.get("/attempts/{attempt_id}")
def review_attempt(attempt_id: str) -> dict[str, Any]:
    """A quiz with every question, your answer and (once answered or
    finished) the right one."""
    store = get_store()
    attempt = _attempt_or_404(attempt_id)
    questions = []
    for public, (lesson_id, qid, perm) in zip(quiz.questions_for(store, attempt["items"]), attempt["items"]):
        lesson = store.lesson(lesson_id)
        q = quiz._question(lesson, qid) if lesson else None
        result = attempt["answers"].get(public["id"])
        if q and (attempt["finished_at"] or result):
            order = perm or list(range(len(q.get("options") or [])))
            public.update(result=result, explanation=q.get("explanation"), model_answer=q.get("model_answer"),
                          answer_index=order.index(q["answer_index"]) if q["kind"] == "mcq" else None)
        questions.append(public)
    lesson = store.lesson(attempt["lesson_id"]) if attempt["lesson_id"] else None
    return {**{k: attempt[k] for k in ("id", "kind", "lesson_id", "course_id", "started_at", "finished_at", "correct", "total", "score", "xp")},
            "lesson_title": lesson["title"] if lesson else "", "questions": questions}


@router.get("/review")
def review_status() -> dict[str, Any]:
    return spaced.status(get_store())


@router.post("/review", status_code=201)
def start_review() -> dict[str, Any]:
    started = quiz.start_review(get_store())
    if started is None:
        raise HTTPException(409, "Nothing is due for review today.")
    return started


# -- progress --------------------------------------------------------------------


@router.get("/history")
def history(days: int = Query(182, ge=7, le=730), before: int | None = None) -> dict[str, Any]:
    return progress.history(get_store(), days=days, before=before)


@router.get("/achievements")
def get_achievements() -> dict[str, Any]:
    store = get_store()
    board = achievements.board(store)
    return {"achievements": board, "unlocked": sum(1 for a in board if a["unlocked_at"]), "total": len(board),
            "level": progress.level_for(sum(store.xp_by_day().values())), "streak": progress.streak(store)}


# -- settings and usage ------------------------------------------------------------


def _usage() -> dict[str, Any]:
    store = get_store()
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    totals = store.one("SELECT COUNT(*) AS calls, COALESCE(SUM(cost), 0) AS cost, COALESCE(SUM(input_tokens + cache_read_tokens"
                       " + cache_write_tokens), 0) AS input, COALESCE(SUM(output_tokens), 0) AS output FROM usage") or {}
    this_month = store.one("SELECT COALESCE(SUM(cost), 0) AS cost FROM usage WHERE ts LIKE ?", f"{month}%") or {}
    by_course = store.all(
        "SELECT u.course_id, COALESCE(c.title, 'Deleted course') AS title, SUM(u.cost) AS cost, COUNT(*) AS calls"
        " FROM usage u LEFT JOIN courses c ON c.id = u.course_id WHERE u.course_id IS NOT NULL"
        " GROUP BY u.course_id ORDER BY cost DESC LIMIT 10")
    by_purpose = store.all("SELECT purpose, SUM(cost) AS cost, COUNT(*) AS calls FROM usage GROUP BY purpose ORDER BY cost DESC")
    return {"calls": totals.get("calls", 0), "cost": round(totals.get("cost", 0), 4), "month": round(this_month.get("cost", 0), 4),
            "input_tokens": totals.get("input", 0), "output_tokens": totals.get("output", 0),
            "by_course": [{**r, "cost": round(r["cost"], 4)} for r in by_course],
            "by_purpose": [{**r, "cost": round(r["cost"], 4)} for r in by_purpose]}


@router.get("/settings")
def get_settings() -> dict[str, Any]:
    from app import push

    store = get_store()
    return {
        "daily_goal": progress.daily_goal(store),
        "llm": llm.describe(),
        "brain": {"configured": siris.brain_configured(), "enabled": siris.brain_enabled(store)},
        "sirisos_url": siris.sirisos_url() or None,
        "push": push.status(store),
        "usage": _usage(),
        "today": local_day(),
    }


@router.put("/settings")
def put_settings(body: Settings) -> dict[str, Any]:
    store = get_store()
    if body.daily_goal is not None:
        store.set_setting("daily_goal", str(body.daily_goal))
    if body.brain_capture is not None:
        store.set_setting("brain_capture", "on" if body.brain_capture else "off")
    return get_settings()


# -- push notifications ----------------------------------------------------------------


class Subscription(BaseModel):
    endpoint: str = Field(max_length=2000)
    keys: dict[str, str]
    expirationTime: float | None = None


class Unsubscribe(BaseModel):
    endpoint: str = Field(max_length=2000)


@router.get("/push/key")
def push_key() -> dict[str, str]:
    from app import push

    return {"key": push.public_key()}


@router.post("/push/subscribe", status_code=201)
def push_subscribe(body: Subscription) -> dict[str, Any]:
    from app import push

    try:
        push.subscribe(get_store(), body.model_dump())
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return push.status(get_store())


@router.post("/push/unsubscribe")
def push_unsubscribe(body: Unsubscribe) -> dict[str, Any]:
    from app import push

    push.unsubscribe(get_store(), body.endpoint)
    return push.status(get_store())


@router.post("/push/test")
async def push_test() -> dict[str, Any]:
    from app import push

    sent = await push.send(get_store(), "SirisLearn notifications are on", "You'll get streak and review reminders here.", tag="test")
    if not sent:
        raise HTTPException(409, "No device accepted the notification. Turn notifications on again on this device.")
    return {"sent": sent}
