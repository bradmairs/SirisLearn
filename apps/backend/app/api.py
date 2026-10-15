"""The web app's API: courses, lessons, quizzes, progress, history,
achievements and settings. Every route needs the signed-in user."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, Field

from app import achievements, generator, progress, quiz
from app.auth import require_user
from app.db import get_store, now_iso

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


class Settings(BaseModel):
    daily_goal: int = Field(ge=10, le=1000)


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
                                  "created_at", "updated_at", "completed_at")},
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


# -- courses -------------------------------------------------------------------


@router.get("/courses")
def list_courses() -> list[dict[str, Any]]:
    return [_course_card(c) for c in get_store().courses()]


@router.post("/courses", status_code=201)
async def create_course(body: NewCourse) -> dict[str, Any]:
    return _course_card(generator.create_course(body.topic, body.level, body.length, body.notes))


@router.get("/courses/{course_id}")
def get_course(course_id: str) -> dict[str, Any]:
    course = _course_or_404(course_id)
    lessons = get_store().lessons(course_id)
    sections = [
        {**s, "lessons": [_lesson_summary(l) for l in lessons if l["section_idx"] == i]}
        for i, s in enumerate(course["sections"])
    ]
    return {**_course_card(course), "notes": course["notes"], "sections": sections}


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
        content = {k: v for k, v in lesson["content"].items() if k != "questions"}
        content["question_count"] = len(lesson["content"]["questions"])
    siblings = store.lessons(lesson["course_id"])
    index = next(i for i, l in enumerate(siblings) if l["id"] == lesson_id)
    return {
        **_lesson_summary(lesson),
        "course": {"id": course["id"], "title": course["title"], "icon": course["icon"]},
        "section": course["sections"][lesson["section_idx"]]["title"] if course["sections"] else "",
        "number": index + 1,
        "of": len(siblings),
        "previous_id": siblings[index - 1]["id"] if index > 0 else None,
        "next_id": siblings[index + 1]["id"] if index + 1 < len(siblings) else None,
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
def start_quiz(lesson_id: str) -> dict[str, Any]:
    lesson = _lesson_or_404(lesson_id)
    if lesson["status"] != "ready":
        raise HTTPException(409, "This lesson isn't written yet.")
    return quiz.start(get_store(), lesson)


@router.get("/lessons/{lesson_id}/attempts")
def lesson_attempts(lesson_id: str) -> list[dict[str, Any]]:
    _lesson_or_404(lesson_id)
    rows = get_store().all(
        "SELECT id, started_at, finished_at, correct, total, score, xp FROM attempts"
        " WHERE lesson_id = ? AND finished_at IS NOT NULL ORDER BY finished_at DESC", lesson_id)
    return rows


# -- quiz attempts ---------------------------------------------------------------


def _attempt_or_404(attempt_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    store = get_store()
    attempt = store.attempt(attempt_id)
    lesson = store.lesson(attempt["lesson_id"]) if attempt else None
    if attempt is None or lesson is None or lesson["status"] != "ready":
        raise HTTPException(404, "No such quiz.")
    return attempt, lesson


@router.post("/attempts/{attempt_id}/answer")
async def answer(attempt_id: str, body: Answer) -> dict[str, Any]:
    attempt, lesson = _attempt_or_404(attempt_id)
    if attempt["finished_at"]:
        raise HTTPException(409, "This quiz is already finished.")
    if body.question_id in attempt["answers"]:
        raise HTTPException(409, "You've already answered this question.")
    question = next((q for q in lesson["content"]["questions"] if q["id"] == body.question_id), None)
    if question is None:
        raise HTTPException(404, "No such question.")
    try:
        return await quiz.answer(get_store(), attempt, question, body.choice, body.text)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.post("/attempts/{attempt_id}/finish")
def finish(attempt_id: str) -> dict[str, Any]:
    attempt, lesson = _attempt_or_404(attempt_id)
    if attempt["finished_at"]:
        raise HTTPException(409, "This quiz is already finished.")
    return quiz.finish(get_store(), attempt, lesson)


@router.get("/attempts/{attempt_id}")
def review(attempt_id: str) -> dict[str, Any]:
    """A finished quiz, with every question, your answer and the right one."""
    attempt, lesson = _attempt_or_404(attempt_id)
    questions = []
    for q in lesson["content"]["questions"]:
        entry = quiz.public_question(q)
        result = attempt["answers"].get(q["id"])
        if attempt["finished_at"] or result:
            entry.update(result=result, explanation=q.get("explanation"), answer_index=q.get("answer_index"),
                         model_answer=q.get("model_answer"))
        questions.append(entry)
    return {**{k: attempt[k] for k in ("id", "lesson_id", "course_id", "started_at", "finished_at", "correct", "total", "score", "xp")},
            "lesson_title": lesson["title"], "questions": questions}


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


@router.get("/settings")
def get_settings() -> dict[str, Any]:
    from app import llm

    return {"daily_goal": progress.daily_goal(get_store()), "llm": llm.describe()}


@router.put("/settings")
def put_settings(body: Settings) -> dict[str, Any]:
    get_store().set_setting("daily_goal", str(body.daily_goal))
    return get_settings()
