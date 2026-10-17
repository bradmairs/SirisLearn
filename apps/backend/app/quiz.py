"""Quizzes of three kinds, all answered one question at a time (each marked
straight away, with an explanation) and then finished to bank the XP:

- **lesson**: 10 questions from the lesson's pool. The pool grows: after
  each attempt a fresh set is written in the background (when a model is
  set up), and a quiz prefers questions you haven't seen. Questions you
  have seen come back with their options shuffled.
- **review**: up to 10 due cards from the spaced-repetition queue, across
  every course (app/spaced.py).
- **exam**: a course's final exam, 20 questions drawn from all its lessons;
  80% passes and earns the certificate.

A question is referred to as "<lesson id>:<question id>". Answers never
reach the browser before the question is answered. Multiple choice is
marked here; open answers by the model against the lesson's key points, or
by key-point matching when no model is set up or the call fails.
"""

from __future__ import annotations

import logging
import random
import re
from collections import Counter
from typing import Any

from app import achievements, prompts, spaced
from app.db import Store, local_day, new_id, now_iso
from app.llm import LLMError, get_llm
from app.progress import (EXAM_PASS_MARK, PASS_MARK, XP_COURSE, XP_EXAM, XP_MCQ, XP_OPEN, XP_OPEN_PARTIAL, XP_PASS, XP_PERFECT,
                          XP_REVIEW_CORRECT, XP_REVIEW_DONE, XP_REVIEW_PARTIAL, course_progress, daily_goal, level_for, streak)

logger = logging.getLogger(__name__)

SCORES = {"correct": 1.0, "partial": 0.5, "incorrect": 0.0}
STOPWORDS = set("a an and are as at be by for from has have in is it its of on or that the their them this to was were will with".split())
QUIZ_SIZE = 10
EXAM_SIZE = 20


# -- questions -----------------------------------------------------------------


def ref(lesson_id: str, qid: str) -> str:
    return f"{lesson_id}:{qid}"


def public_question(q: dict[str, Any], lesson_id: str, perm: list[int] | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"id": ref(lesson_id, q["id"]), "kind": q["kind"], "prompt": q["prompt"], "svg": q.get("svg") or "",
                           "image_alt": q.get("image_alt") or ""}
    if q["kind"] == "mcq":
        order = perm or list(range(len(q["options"])))
        out["options"] = [q["options"][i] for i in order]
    return out


def _question(lesson: dict[str, Any], qid: str) -> dict[str, Any] | None:
    return next((q for q in (lesson.get("content") or {}).get("questions") or [] if q["id"] == qid), None)


def _seen(store: Store, lesson_id: str) -> Counter:
    counts: Counter = Counter()
    for a in store.all("SELECT items FROM attempts WHERE items LIKE ?", f"%{lesson_id}%"):
        for item in a["items"]:
            if item[0] == lesson_id:
                counts[item[1]] += 1
    return counts


def _item(lesson: dict[str, Any], q: dict[str, Any], shuffle: bool) -> list[Any]:
    perm = list(range(len(q.get("options") or [])))
    if shuffle and q["kind"] == "mcq":
        random.shuffle(perm)
    return [lesson["id"], q["id"], perm]


def pick_for_lesson(store: Store, lesson: dict[str, Any], size: int = QUIZ_SIZE) -> tuple[list[list[Any]], bool]:
    """Unseen questions first (in lesson order), then the least seen."""
    pool = lesson["content"]["questions"]
    seen = _seen(store, lesson["id"])
    ranked = sorted(pool, key=lambda q: (seen[q["id"]], random.random()))[:size]
    order = {q["id"]: i for i, q in enumerate(pool)}
    chosen = sorted(ranked, key=lambda q: order[q["id"]])
    fresh = all(seen[q["id"]] == 0 for q in chosen)
    return [_item(lesson, q, shuffle=seen[q["id"]] > 0) for q in chosen], fresh


def unseen_count(store: Store, lesson: dict[str, Any]) -> int:
    seen = _seen(store, lesson["id"])
    return sum(1 for q in lesson["content"]["questions"] if not seen[q["id"]])


# -- starting ------------------------------------------------------------------


def _create(store: Store, kind: str, items: list[list[Any]], lesson_id: str = "", course_id: str = "") -> dict[str, Any]:
    attempt = {"id": new_id(), "kind": kind, "lesson_id": lesson_id, "course_id": course_id, "started_at": now_iso(),
               "total": len(items), "items": items, "answers": {}}
    store.insert("attempts", attempt)
    return attempt


def questions_for(store: Store, items: list[list[Any]]) -> list[dict[str, Any]]:
    lessons: dict[str, dict[str, Any]] = {}
    out = []
    for lesson_id, qid, perm in items:
        lesson = lessons.get(lesson_id) or store.lesson(lesson_id)
        if lesson is None:
            continue
        lessons[lesson_id] = lesson
        q = _question(lesson, qid)
        if q:
            out.append({**public_question(q, lesson_id, perm), "lesson_title": lesson["title"]})
    return out


def start_lesson(store: Store, lesson: dict[str, Any]) -> dict[str, Any]:
    items, fresh = pick_for_lesson(store, lesson)
    attempt = _create(store, "lesson", items, lesson["id"], lesson["course_id"])
    return {"attempt_id": attempt["id"], "kind": "lesson", "fresh": fresh, "questions": questions_for(store, items)}


def start_review(store: Store) -> dict[str, Any] | None:
    cards = spaced.due_cards(store)
    items = []
    for card in cards:
        lesson = store.lesson(card["lesson_id"])
        q = _question(lesson, card["qid"]) if lesson else None
        if q:
            items.append(_item(lesson, q, shuffle=True))  # type: ignore[arg-type]
    if not items:
        return None
    random.shuffle(items)
    attempt = _create(store, "review", items)
    return {"attempt_id": attempt["id"], "kind": "review", "questions": questions_for(store, items)}


def start_exam(store: Store, course: dict[str, Any]) -> dict[str, Any]:
    lessons = [l for l in store.lessons(course["id"]) if l["status"] == "ready"]
    per = max(1, -(-EXAM_SIZE // max(1, len(lessons))))  # ceil
    items: list[list[Any]] = []
    for lesson in lessons:
        pool = list(lesson["content"]["questions"])
        random.shuffle(pool)
        items += [_item(lesson, q, shuffle=True) for q in pool[:per]]
    random.shuffle(items)
    items = items[:EXAM_SIZE]
    attempt = _create(store, "exam", items, course_id=course["id"])
    return {"attempt_id": attempt["id"], "kind": "exam", "questions": questions_for(store, items)}


# -- answering -----------------------------------------------------------------


def _xp(kind: str, question_kind: str, verdict: str) -> int:
    if kind == "exam":
        return 0
    if kind == "review":
        return {"correct": XP_REVIEW_CORRECT, "partial": XP_REVIEW_PARTIAL}.get(verdict, 0)
    if question_kind == "mcq":
        return XP_MCQ if verdict == "correct" else 0
    return {"correct": XP_OPEN, "partial": XP_OPEN_PARTIAL}.get(verdict, 0)


async def answer(store: Store, attempt: dict[str, Any], question_ref: str, choice: int | None, text: str | None) -> dict[str, Any]:
    item = next((i for i in attempt["items"] if ref(i[0], i[1]) == question_ref), None)
    if item is None:
        raise LookupError("That question isn't in this quiz.")
    lesson = store.lesson(item[0])
    question = _question(lesson, item[1]) if lesson else None
    if lesson is None or question is None:
        raise LookupError("That question no longer exists.")
    perm = item[2] or list(range(len(question.get("options") or [])))
    if question["kind"] == "mcq":
        if choice is None or not 0 <= choice < len(perm):
            raise ValueError("Pick one of the options.")
        verdict = "correct" if perm[choice] == question["answer_index"] else "incorrect"
        result: dict[str, Any] = {"verdict": verdict, "choice": choice, "answer_index": perm.index(question["answer_index"]), "feedback": ""}
    else:
        text = (text or "").strip()
        if not text:
            raise ValueError("Write an answer first.")
        verdict, feedback, marked_by = await mark_open(question, text[:4000], lesson)
        result = {"verdict": verdict, "text": text[:4000], "feedback": feedback, "marked_by": marked_by,
                  "model_answer": question["model_answer"], "key_points": question.get("key_points") or []}
    result.update(kind=question["kind"], image=bool(question.get("svg")), score=SCORES[result["verdict"]],
                  xp=_xp(attempt["kind"], question["kind"], result["verdict"]), explanation=question.get("explanation") or "",
                  lesson_id=lesson["id"], lesson_title=lesson["title"])
    result["review"] = spaced.record(store, lesson, question["id"], result["verdict"])
    answers = dict(attempt["answers"], **{question_ref: result})
    store.update("attempts", attempt["id"], answers=answers)
    return result


async def mark_open(question: dict[str, Any], text: str, lesson: dict[str, Any] | None = None) -> tuple[str, str, str]:
    llm = get_llm()
    if llm is not None:
        try:
            graded = await llm.json(system=prompts.GRADER_SYSTEM, context="", prompt=prompts.grade_prompt(question, text),
                                    schema=prompts.GRADE_SCHEMA, effort="low", max_tokens=4000,
                                    meta={"purpose": "mark", "course_id": (lesson or {}).get("course_id"), "lesson_id": (lesson or {}).get("id")})
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
    said = {w[:5] for w in _words(text)}
    hits = []
    for point in points:
        stems = {w[:5] for w in _words(point)}
        if stems and len(said & stems) / len(stems) >= 0.5:
            hits.append(point)
    share = len(hits) / len(points) if points else 0
    model = {w[:5] for w in _words(question.get("model_answer") or "")}
    if model and len(said & model) / len(model) >= 0.6:  # says what the model answer says
        share = 1.0
    verdict = "correct" if share >= 0.67 else "partial" if share >= 0.34 else "incorrect"
    missing = [p for p in points if p not in hits] if share < 1 else []
    feedback = "Marked offline against the key points." + (f" Missing: {'; '.join(missing)}." if missing else "")
    return verdict, feedback


# -- finishing -----------------------------------------------------------------


def _score(attempt: dict[str, Any]) -> tuple[float, int, float]:
    total = attempt["total"] or len(attempt["items"])
    correct = sum(a["score"] for a in attempt["answers"].values())
    return correct, total, (correct / total if total else 0)


def _wrap_up(store: Store, attempt: dict[str, Any], before: dict[str, Any], goal_was_met: bool, xp: int,
             bonus: list[dict[str, Any]], extra: dict[str, Any]) -> dict[str, Any]:
    today_xp = store.xp_by_day().get(local_day(), 0)
    goal = daily_goal(store)
    if today_xp >= goal and not goal_was_met:
        store.log("goal_met", title=f"Daily goal: {goal} XP", detail={"goal": goal})
    unlocked = achievements.check(store)
    after = level_for(sum(store.xp_by_day().values()))
    correct, total, score = _score(attempt)
    return {
        "attempt_id": attempt["id"],
        "kind": attempt["kind"],
        "correct": correct,
        "total": total,
        "score": round(score, 3),
        "xp": xp + sum(b["xp"] for b in bonus if not b.get("included")),
        "bonus": bonus,
        "streak": streak(store),
        "goal": {"goal": goal, "today": today_xp, "met_now": today_xp >= goal and not goal_was_met},
        "level": after,
        "level_up": after["level"] > before["level"],
        "achievements": unlocked,
        **extra,
    }


def finish(store: Store, attempt: dict[str, Any]) -> dict[str, Any]:
    before = level_for(sum(store.xp_by_day().values()))
    goal_was_met = store.xp_by_day().get(local_day(), 0) >= daily_goal(store)
    correct, total, score = _score(attempt)
    xp = sum(a["xp"] for a in attempt["answers"].values())
    finished = now_iso()
    bonus: list[dict[str, Any]] = []
    extra: dict[str, Any] = {}

    if attempt["kind"] == "review":
        xp += XP_REVIEW_DONE
        bonus.append({"label": "Daily review", "xp": XP_REVIEW_DONE, "included": True})
        store.update("attempts", attempt["id"], finished_at=finished, correct=correct, score=round(score, 3), xp=xp)
        store.log("review_finished", title=f"Daily review: {total} card{'s' if total != 1 else ''}", xp=xp,
                  detail={"attempt_id": attempt["id"], "correct": correct, "total": total})
        extra = {"passed": True}

    elif attempt["kind"] == "exam":
        course = store.course(attempt["course_id"]) or {"id": attempt["course_id"], "title": "", "exam_passed_at": None, "exam_best": None}
        passed = score >= EXAM_PASS_MARK
        first = passed and not course.get("exam_passed_at")
        if first:
            xp += XP_EXAM
            bonus.append({"label": "Final exam passed", "xp": XP_EXAM, "included": True})
        store.update("attempts", attempt["id"], finished_at=finished, correct=correct, score=round(score, 3), xp=xp)
        store.update("courses", course["id"], exam_best=round(max(score, course.get("exam_best") or 0), 3),
                     exam_passed_at=finished if first else course.get("exam_passed_at"))
        store.log("exam_finished", title=f"Final exam: {course['title']}", course=course, xp=xp,
                  detail={"attempt_id": attempt["id"], "correct": correct, "total": total, "passed": passed, "first_pass": first})
        extra = {"passed": passed, "first_pass": first, "course_id": course["id"], "certificate": first or bool(course.get("exam_passed_at"))}

    else:
        lesson = store.lesson(attempt["lesson_id"])
        course = store.course(attempt["course_id"]) or {"id": attempt["course_id"], "title": ""}
        perfect = total > 0 and correct >= total
        if perfect:
            xp += XP_PERFECT
            bonus.append({"label": "Perfect score", "xp": XP_PERFECT, "included": True})
        passed = score >= PASS_MARK
        store.update("attempts", attempt["id"], finished_at=finished, correct=correct, score=round(score, 3), xp=xp)
        store.log("quiz_finished", title=lesson["title"] if lesson else "", course=course, lesson_id=attempt["lesson_id"], xp=xp,
                  detail={"attempt_id": attempt["id"], "correct": correct, "total": total, "perfect": perfect, "passed": passed})
        first_pass = bool(lesson) and passed and not lesson["passed_at"]  # type: ignore[index]
        if lesson:
            store.update("lessons", lesson["id"], best_score=round(max(score, lesson["best_score"] or 0), 3),
                         passed_at=finished if first_pass else lesson["passed_at"])
        if first_pass:
            store.log("lesson_passed", title=lesson["title"], course=course, lesson_id=lesson["id"], xp=XP_PASS)  # type: ignore[index]
            bonus.append({"label": "Lesson passed", "xp": XP_PASS})
            progress = course_progress(store, course["id"])
            if progress["lessons"] and progress["passed"] == progress["lessons"] and not course.get("completed_at"):
                store.update("courses", course["id"], completed_at=finished)
                store.log("course_completed", title=course["title"], course=course, xp=XP_COURSE)
                bonus.append({"label": "Course complete", "xp": XP_COURSE})
        store.touch_course(course["id"])
        extra = {"passed": passed, "first_pass": first_pass, "lesson_id": attempt["lesson_id"],
                 "course_completed": any(b["label"] == "Course complete" for b in bonus)}

    return _wrap_up(store, attempt, before, goal_was_met, xp, bonus, extra)
