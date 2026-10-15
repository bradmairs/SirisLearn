"""Taking a quiz: start an attempt, answer one question at a time (each is
marked straight away, with an explanation), then finish to bank the XP.

Answers never reach the browser before the question is answered. Multiple
choice is marked here; open answers are marked by the model against the
lesson's key points, or by key-point matching when no model is set up or
the call fails.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from app import achievements, prompts
from app.db import Store, local_day, new_id, now_iso
from app.llm import LLMError, get_llm
from app.progress import (PASS_MARK, XP_COURSE, XP_MCQ, XP_OPEN, XP_OPEN_PARTIAL, XP_PASS, XP_PERFECT, course_progress,
                          daily_goal, level_for, streak)

logger = logging.getLogger(__name__)

SCORES = {"correct": 1.0, "partial": 0.5, "incorrect": 0.0}
STOPWORDS = set("a an and are as at be by for from has have in is it its of on or that the their them this to was were will with".split())


def public_question(q: dict[str, Any]) -> dict[str, Any]:
    keep = ("id", "kind", "prompt", "svg", "image_alt", "options")
    return {k: q[k] for k in keep if k in q}


def start(store: Store, lesson: dict[str, Any]) -> dict[str, Any]:
    attempt = {"id": new_id(), "lesson_id": lesson["id"], "course_id": lesson["course_id"], "started_at": now_iso(),
               "total": len(lesson["content"]["questions"]), "answers": {}}
    store.insert("attempts", attempt)
    return {"attempt_id": attempt["id"], "questions": [public_question(q) for q in lesson["content"]["questions"]]}


async def answer(store: Store, attempt: dict[str, Any], question: dict[str, Any], choice: int | None, text: str | None) -> dict[str, Any]:
    if question["kind"] == "mcq":
        if choice is None or not 0 <= choice < len(question["options"]):
            raise ValueError("Pick one of the options.")
        verdict = "correct" if choice == question["answer_index"] else "incorrect"
        result = {"verdict": verdict, "choice": choice, "answer_index": question["answer_index"],
                  "feedback": "", "xp": XP_MCQ if verdict == "correct" else 0}
    else:
        text = (text or "").strip()
        if not text:
            raise ValueError("Write an answer first.")
        verdict, feedback, marked_by = await mark_open(question, text[:4000])
        result = {"verdict": verdict, "text": text[:4000], "feedback": feedback, "marked_by": marked_by,
                  "model_answer": question["model_answer"], "key_points": question.get("key_points") or [],
                  "xp": {"correct": XP_OPEN, "partial": XP_OPEN_PARTIAL}.get(verdict, 0)}
    result.update(kind=question["kind"], image=bool(question.get("svg")), score=SCORES[result["verdict"]],
                  explanation=question.get("explanation") or "")
    answers = dict(attempt["answers"], **{question["id"]: result})
    store.update("attempts", attempt["id"], answers=answers)
    return result


async def mark_open(question: dict[str, Any], text: str) -> tuple[str, str, str]:
    llm = get_llm()
    if llm is not None:
        try:
            graded = await llm.json(system=prompts.GRADER_SYSTEM, context="", prompt=prompts.grade_prompt(question, text),
                                    schema=prompts.GRADE_SCHEMA, effort="low", max_tokens=4000)
            if graded.get("verdict") in SCORES:
                return graded["verdict"], str(graded.get("feedback") or "").strip(), "model"
        except LLMError:
            logger.warning("Model marking failed; falling back to key points", exc_info=True)
    return (*mark_by_key_points(question, text), "key points")


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS and len(w) > 2}


def mark_by_key_points(question: dict[str, Any], text: str) -> tuple[str, str]:
    """Offline fallback: how many key points the answer mentions."""
    points = question.get("key_points") or [question.get("model_answer") or ""]
    said = _words(text)
    hits = []
    for point in points:
        words = _words(point)
        stems = {w[:5] for w in words}
        if words and len({w[:5] for w in said} & stems) / len(stems) >= 0.5:
            hits.append(point)
    share = len(hits) / len(points) if points else 0
    verdict = "correct" if share >= 0.67 else "partial" if share >= 0.34 else "incorrect"
    missing = [p for p in points if p not in hits]
    feedback = "Marked offline against the key points." + (f" Missing: {'; '.join(missing)}." if missing else "")
    return verdict, feedback


def finish(store: Store, attempt: dict[str, Any], lesson: dict[str, Any]) -> dict[str, Any]:
    course = store.course(lesson["course_id"]) or {"id": lesson["course_id"], "title": ""}
    before = level_for(sum(store.xp_by_day().values()))
    goal_was_met = store.xp_by_day().get(local_day(), 0) >= daily_goal(store)

    answers = attempt["answers"]
    total = attempt["total"] or len(lesson["content"]["questions"])
    correct = sum(a["score"] for a in answers.values())
    score = correct / total if total else 0
    xp = sum(a["xp"] for a in answers.values())
    perfect = total > 0 and correct >= total
    if perfect:
        xp += XP_PERFECT
    finished = now_iso()
    store.update("attempts", attempt["id"], finished_at=finished, correct=correct, score=round(score, 3), xp=xp)
    store.log("quiz_finished", title=lesson["title"], course=course, lesson_id=lesson["id"], xp=xp,
              detail={"attempt_id": attempt["id"], "correct": correct, "total": total, "perfect": perfect})

    bonus: list[dict[str, Any]] = []
    first_pass = score >= PASS_MARK and not lesson["passed_at"]
    best = max(score, lesson["best_score"] or 0)
    store.update("lessons", lesson["id"], best_score=round(best, 3), passed_at=finished if first_pass else lesson["passed_at"])
    if first_pass:
        store.log("lesson_passed", title=lesson["title"], course=course, lesson_id=lesson["id"], xp=XP_PASS)
        bonus.append({"label": "Lesson passed", "xp": XP_PASS})
        progress = course_progress(store, course["id"])
        if progress["lessons"] and progress["passed"] == progress["lessons"] and not course.get("completed_at"):
            store.update("courses", course["id"], completed_at=finished)
            store.log("course_completed", title=course["title"], course=course, xp=XP_COURSE)
            bonus.append({"label": "Course complete", "xp": XP_COURSE})
    if perfect:
        bonus.append({"label": "Perfect score", "xp": XP_PERFECT})
    store.touch_course(course["id"])

    today_xp = store.xp_by_day().get(local_day(), 0)
    goal = daily_goal(store)
    if today_xp >= goal and not goal_was_met:
        store.log("goal_met", title=f"Daily goal: {goal} XP", detail={"goal": goal})
    unlocked = achievements.check(store)
    after = level_for(sum(store.xp_by_day().values()))
    return {
        "attempt_id": attempt["id"],
        "correct": correct,
        "total": total,
        "score": round(score, 3),
        "passed": score >= PASS_MARK,
        "first_pass": first_pass,
        "xp": xp + sum(b["xp"] for b in bonus if b["label"] != "Perfect score"),
        "bonus": bonus,
        "streak": streak(store),
        "goal": {"goal": goal, "today": today_xp, "met_now": today_xp >= goal and not goal_was_met},
        "level": after,
        "level_up": after["level"] > before["level"],
        "achievements": unlocked,
        "course_completed": any(b["label"] == "Course complete" for b in bonus),
    }
