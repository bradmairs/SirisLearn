"""Weak spots: how well you answer each lesson's questions, and each kind of
question, over the last SIRISLEARN_INSIGHT_DAYS (default 90).

Every answer in every quiz counts (lesson quizzes, reviews, practice and
exams). A lesson is a weak spot once it has at least MIN_ANSWERS answers and
under WEAK_BELOW right. The daily review serves weak lessons' cards first
when more are due than fit in one review (app/spaced.py), and a weak spot
can be drilled with a practice round (quiz.start_practice).
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from app import config
from app.db import Store

MIN_ANSWERS = 4
WEAK_BELOW = 0.7
KIND_LABELS = {"mcq": "Multiple choice", "open": "Written", "scenario": "Scenario", "calc": "Calculation", "picture": "Picture questions"}


def days() -> int:
    return max(7, int(config.env("SIRISLEARN_INSIGHT_DAYS", "90")))


def _answers(store: Store) -> list[dict[str, Any]]:
    since = (datetime.now(timezone.utc) - timedelta(days=days())).isoformat(timespec="seconds")
    out = []
    for attempt in store.all("SELECT answers, started_at FROM attempts WHERE started_at >= ?", since):
        for result in attempt["answers"].values():
            if result.get("lesson_id"):
                out.append({**result, "at": attempt["started_at"]})
    return out


def lesson_scores(store: Store) -> dict[str, dict[str, Any]]:
    """Per lesson: answers, average score and the last time it was answered."""
    totals: dict[str, dict[str, Any]] = defaultdict(lambda: {"answered": 0, "score": 0.0, "last": ""})
    for a in _answers(store):
        t = totals[a["lesson_id"]]
        t["answered"] += 1
        t["score"] += a.get("score", 0)
        t["last"] = max(t["last"], a["at"])
    return {k: {**v, "accuracy": v["score"] / v["answered"]} for k, v in totals.items()}


def weak_lessons(store: Store) -> set[str]:
    return {k for k, v in lesson_scores(store).items() if v["answered"] >= MIN_ANSWERS and v["accuracy"] < WEAK_BELOW}


def report(store: Store) -> dict[str, Any]:
    scores = lesson_scores(store)
    lessons = {l["id"]: l for l in store.all(
        "SELECT l.id, l.title, l.course_id, l.status, c.title AS course_title, c.icon FROM lessons l"
        " JOIN courses c ON c.id = l.course_id WHERE c.archived = 0")}
    rows = []
    for lesson_id, s in scores.items():
        lesson = lessons.get(lesson_id)
        if lesson is None or s["answered"] < MIN_ANSWERS:
            continue
        due = store.one("SELECT COUNT(*) AS n FROM reviews WHERE lesson_id = ? AND box = 0", lesson_id) or {"n": 0}
        rows.append({"lesson_id": lesson_id, "title": lesson["title"], "course_id": lesson["course_id"],
                     "course_title": lesson["course_title"], "icon": lesson["icon"], "answered": s["answered"],
                     "accuracy": round(s["accuracy"], 3), "last": s["last"], "missed": due["n"],
                     "ready": lesson["status"] == "ready"})
    rows.sort(key=lambda r: (r["accuracy"], -r["answered"]))
    kinds: dict[str, list[float]] = defaultdict(list)
    answers = _answers(store)
    for a in answers:
        kinds[a.get("kind") or "mcq"].append(a.get("score", 0))
        if a.get("image"):
            kinds["picture"].append(a.get("score", 0))
    return {
        "days": days(),
        "answered": len(answers),
        "weak": [r for r in rows if r["accuracy"] < WEAK_BELOW][:10],
        "strong": [r for r in reversed(rows) if r["accuracy"] >= 0.9][:5],
        "kinds": [{"kind": k, "label": KIND_LABELS[k], "answered": len(v), "accuracy": round(sum(v) / len(v), 3)}
                  for k, v in kinds.items() if k in KIND_LABELS and v],
        "min_answers": MIN_ANSWERS,
        "weak_below": WEAK_BELOW,
    }
