"""Achievements: what they are, how far along each one is, and unlocking them.

Each achievement measures one number from `stats()` against a target, so the
Awards screen can show progress ("4 / 7 days") on the locked ones too.
They're checked after every quiz; each unlock is logged in the history once.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from typing import Any

from app import config
from app.db import Store
from app.progress import active_days, daily_goal, walk

# id, title, description, icon (lucide), stat, target, tier
CATALOGUE: list[tuple[str, str, str, str, str, int, str]] = [
    ("first-steps", "First steps", "Finish your first quiz.", "footprints", "quizzes", 1, "bronze"),
    ("curious-mind", "Curious mind", "Start 5 courses.", "lightbulb", "courses_created", 5, "silver"),
    ("polymath", "Polymath", "Pass lessons in 5 different courses.", "shapes", "courses_touched", 5, "gold"),
    ("on-a-roll", "On a roll", "Keep a 3-day streak.", "flame", "best_streak", 3, "bronze"),
    ("week-warrior", "Week warrior", "Keep a 7-day streak.", "flame", "best_streak", 7, "silver"),
    ("fortnight", "Fortnight focus", "Keep a 14-day streak.", "flame", "best_streak", 14, "silver"),
    ("monthly-mind", "Monthly mind", "Keep a 30-day streak.", "flame", "best_streak", 30, "gold"),
    ("centurion", "Centurion", "Keep a 100-day streak.", "crown", "best_streak", 100, "platinum"),
    ("perfect-10", "Perfect 10", "Score 10 out of 10 on a quiz.", "target", "perfect_quizzes", 1, "bronze"),
    ("sharpshooter", "Sharpshooter", "Score 10 out of 10 on 10 quizzes.", "crosshair", "perfect_quizzes", 10, "gold"),
    ("graduate", "Graduate", "Finish a course.", "graduation-cap", "courses_completed", 1, "silver"),
    ("scholar", "Scholar", "Finish 5 courses.", "library", "courses_completed", 5, "gold"),
    ("lesson-25", "Steady learner", "Pass 25 lessons.", "book-open-check", "lessons_passed", 25, "silver"),
    ("lesson-100", "Bookworm", "Pass 100 lessons.", "book-marked", "lessons_passed", 100, "gold"),
    ("xp-1000", "Thousand club", "Earn 1,000 XP.", "zap", "xp", 1000, "silver"),
    ("xp-5000", "Powerhouse", "Earn 5,000 XP.", "zap", "xp", 5000, "gold"),
    ("xp-20000", "Luminary", "Earn 20,000 XP.", "sun", "xp", 20000, "platinum"),
    ("wordsmith", "Wordsmith", "Get 25 open-answer questions right.", "pen-line", "open_correct", 25, "silver"),
    ("sharp-eye", "Sharp eye", "Get 25 picture questions right.", "eye", "image_correct", 25, "silver"),
    ("goal-getter", "Goal getter", "Hit your daily goal on 7 days.", "circle-check-big", "goal_days", 7, "silver"),
    ("marathon", "Marathon", "Finish 5 quizzes in one day.", "timer", "max_quizzes_in_day", 5, "silver"),
    ("night-owl", "Night owl", "Finish a quiz after 10 pm.", "moon", "night_quizzes", 1, "bronze"),
    ("early-bird", "Early bird", "Finish a quiz before 7 am.", "sunrise", "early_quizzes", 1, "bronze"),
    ("comeback", "Comeback", "Come back to learning after a week or more away.", "rotate-ccw", "comebacks", 1, "bronze"),
    ("first-review", "Look back", "Finish your first daily review.", "repeat", "reviews", 1, "bronze"),
    ("reviewer", "Spaced out", "Finish 25 daily reviews.", "repeat", "reviews", 25, "silver"),
    ("long-memory", "Long memory", "Get 50 cards to the top box (two months between reviews).", "archive", "top_box", 50, "gold"),
    ("certified", "Certified", "Pass a course's final exam.", "badge-check", "exams_passed", 1, "silver"),
    ("credentialed", "Credentialed", "Pass 5 final exams.", "medal", "exams_passed", 5, "platinum"),
    ("ice-cold", "Ice cold", "Have a streak freeze save your streak.", "snowflake", "freezes_used", 1, "bronze"),
]


def catalogue() -> list[dict[str, Any]]:
    return [
        {"id": i, "title": t, "description": d, "icon": icon, "stat": stat, "target": target, "tier": tier}
        for i, t, d, icon, stat, target, tier in CATALOGUE
    ]


def stats(store: Store) -> dict[str, int]:
    tz = config.timezone()
    attempts = store.finished_attempts("lesson")
    answers = [a for attempt in store.finished_attempts() for a in attempt["answers"].values()]
    finished_local = [datetime.fromisoformat(a["finished_at"]).astimezone(tz) for a in attempts]
    per_day = Counter(t.date() for t in finished_local)
    days = active_days(store)
    state = walk(days)
    gaps = [(date.fromisoformat(b) - date.fromisoformat(a)).days for a, b in zip(days, days[1:])]
    by_day = store.xp_by_day()
    goal = daily_goal(store)
    count = lambda sql: (store.one(sql) or {"n": 0})["n"] or 0  # noqa: E731
    return {
        "quizzes": len(attempts),
        "perfect_quizzes": sum(1 for a in attempts if a["total"] and a["correct"] >= a["total"]),
        "best_streak": state["best"],
        "courses_created": count("SELECT COUNT(*) AS n FROM events WHERE kind = 'course_created'"),
        "courses_completed": count("SELECT COUNT(*) AS n FROM events WHERE kind = 'course_completed'"),
        "courses_touched": count("SELECT COUNT(DISTINCT course_id) AS n FROM events WHERE kind = 'lesson_passed'"),
        "lessons_passed": count("SELECT COUNT(*) AS n FROM events WHERE kind = 'lesson_passed'"),
        "xp": sum(by_day.values()),
        "open_correct": sum(1 for a in answers if a.get("kind") == "open" and a.get("verdict") == "correct"),
        "image_correct": sum(1 for a in answers if a.get("image") and a.get("verdict") == "correct"),
        "goal_days": sum(1 for v in by_day.values() if v >= goal),
        "max_quizzes_in_day": max(per_day.values(), default=0),
        "night_quizzes": sum(1 for t in finished_local if t.hour >= 22),
        "early_quizzes": sum(1 for t in finished_local if 4 <= t.hour < 7),
        "comebacks": sum(1 for g in gaps if g >= 8),
        "reviews": count("SELECT COUNT(*) AS n FROM events WHERE kind = 'review_finished'"),
        "top_box": count("SELECT COUNT(*) AS n FROM reviews WHERE box >= 5"),
        "exams_passed": count("SELECT COUNT(*) AS n FROM courses WHERE exam_passed_at IS NOT NULL"),
        "freezes_used": len(state["frozen"]),
    }


def board(store: Store) -> list[dict[str, Any]]:
    """Every achievement with its progress, unlocked ones first."""
    numbers = stats(store)
    unlocked = store.unlocked()
    out = []
    for a in catalogue():
        value = numbers.get(a["stat"], 0)
        out.append({**a, "value": min(value, a["target"]), "unlocked_at": unlocked.get(a["id"])})
    return sorted(out, key=lambda a: (a["unlocked_at"] is None, -(a["value"] / a["target"])))


def check(store: Store) -> list[dict[str, Any]]:
    """Unlock anything newly earned; returns the new ones."""
    numbers = stats(store)
    unlocked = store.unlocked()
    fresh = []
    for a in catalogue():
        if a["id"] not in unlocked and numbers.get(a["stat"], 0) >= a["target"]:
            store.unlock(a["id"])
            store.log("achievement", title=a["title"], detail={"id": a["id"], "icon": a["icon"], "tier": a["tier"]})
            fresh.append(a)
    return fresh
