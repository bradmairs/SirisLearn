"""XP, levels, streaks, the daily goal and the numbers behind the home screen,
the history page, the achievements and the SirisOS widget.

- **XP** comes from quizzes: 10 per right multiple-choice answer, 15 per
  right open answer (7 for a partly right one), +20 the first time a lesson
  is passed (70%+), +15 for a perfect 10/10, +100 for finishing a course.
- **Level** n needs 50 * n * (n - 1) XP: 100 for level 2, 300 for 3, 600 for 4...
- **Streak**: consecutive days (in SIRISLEARN_TIMEZONE) with at least one
  finished quiz. Until today's quiz is done, yesterday's streak still counts
  but is "at risk".
- **Daily goal**: XP to earn each day (default 50, changeable in Settings).
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
from typing import Any

from app import config
from app.db import Store, local_day

XP_MCQ = 10
XP_OPEN = 15
XP_OPEN_PARTIAL = 7
XP_PASS = 20
XP_PERFECT = 15
XP_COURSE = 100
PASS_MARK = 0.7


def level_for(xp: int) -> dict[str, Any]:
    level = 1
    while 50 * (level + 1) * level <= xp:
        level += 1
    floor, ceiling = 50 * level * (level - 1), 50 * (level + 1) * level
    return {"level": level, "xp_into": xp - floor, "xp_for_next": ceiling - floor, "progress": round((xp - floor) / (ceiling - floor), 3)}


def daily_goal(store: Store) -> int:
    try:
        return max(10, int(store.setting("daily_goal", str(config.default_daily_goal()))))
    except ValueError:
        return config.default_daily_goal()


def active_days(store: Store) -> list[str]:
    return [r["day"] for r in store.all("SELECT DISTINCT day FROM events WHERE kind = 'quiz_finished' ORDER BY day")]


def runs(days: list[str]) -> list[tuple[str, str, int]]:
    """Consecutive runs of days as (first, last, length)."""
    out: list[tuple[str, str, int]] = []
    for day in sorted(set(days)):
        if out and date.fromisoformat(out[-1][1]) + timedelta(days=1) == date.fromisoformat(day):
            first, _, length = out[-1]
            out[-1] = (first, day, length + 1)
        else:
            out.append((day, day, 1))
    return out


def streak(store: Store, today: str | None = None) -> dict[str, Any]:
    today = today or local_day()
    yesterday = (date.fromisoformat(today) - timedelta(days=1)).isoformat()
    all_runs = runs(active_days(store))
    current = 0
    if all_runs and all_runs[-1][1] in (today, yesterday):
        current = all_runs[-1][2]
    done = bool(all_runs) and all_runs[-1][1] == today
    return {
        "current": current,
        "best": max((r[2] for r in all_runs), default=0),
        "today_done": done,
        "at_risk": current > 0 and not done,
    }


def course_progress(store: Store, course_id: str) -> dict[str, Any]:
    row = store.one(
        "SELECT COUNT(*) AS total, SUM(passed_at IS NOT NULL) AS passed, SUM(status = 'ready') AS written,"
        " SUM(status = 'writing') AS writing FROM lessons WHERE course_id = ?",
        course_id,
    ) or {}
    total, passed = row.get("total") or 0, row.get("passed") or 0
    return {"lessons": total, "passed": passed, "written": row.get("written") or 0, "writing": row.get("writing") or 0,
            "percent": round(100 * passed / total) if total else 0}


def next_lesson(store: Store, course_id: str) -> dict[str, Any] | None:
    return store.one(
        "SELECT id, title, status, position FROM lessons WHERE course_id = ? AND passed_at IS NULL ORDER BY position LIMIT 1",
        course_id,
    )


def continue_learning(store: Store) -> dict[str, Any] | None:
    """The next lesson in the course you touched most recently."""
    for course in store.courses():
        if course["status"] != "ready" or course["archived"] or course["completed_at"]:
            continue
        lesson = next_lesson(store, course["id"])
        if lesson:
            return {"course_id": course["id"], "course_title": course["title"], "icon": course["icon"],
                    "lesson_id": lesson["id"], "lesson_title": lesson["title"], "lesson_status": lesson["status"],
                    "progress": course_progress(store, course["id"])}
    return None


def summary(store: Store) -> dict[str, Any]:
    """Home screen and SirisOS widget numbers."""
    from app.achievements import catalogue

    today = local_day()
    by_day = store.xp_by_day()
    total = sum(by_day.values())
    goal = daily_goal(store)
    week_start = (date.fromisoformat(today) - timedelta(days=6)).isoformat()
    courses = store.courses()
    unlocked = store.unlocked()
    recent = sorted(unlocked.items(), key=lambda kv: kv[1], reverse=True)[:3]
    names = {a["id"]: a for a in catalogue()}
    today_events = Counter(e["kind"] for e in store.all("SELECT kind FROM events WHERE day = ?", today))
    return {
        "today": today,
        "streak": streak(store, today),
        "xp": {"total": total, "today": by_day.get(today, 0), "goal": goal, "goal_met": by_day.get(today, 0) >= goal,
               "week": sum(v for d, v in by_day.items() if d >= week_start)},
        "level": level_for(total),
        "courses": {
            "total": len(courses),
            "active": sum(1 for c in courses if c["status"] == "ready" and not c["completed_at"] and not c["archived"]),
            "completed": sum(1 for c in courses if c["completed_at"]),
            "planning": sum(1 for c in courses if c["status"] == "planning"),
        },
        "activity": {"quizzes": today_events["quiz_finished"], "lessons_passed": today_events["lesson_passed"]},
        "continue": continue_learning(store),
        "achievements": {
            "unlocked": len(unlocked), "total": len(names),
            "recent": [{"id": k, "title": names[k]["title"], "icon": names[k]["icon"], "unlocked_at": v} for k, v in recent if k in names],
        },
    }


def history(store: Store, days: int = 182, before: int | None = None, limit: int = 60) -> dict[str, Any]:
    today = date.fromisoformat(local_day())
    by_day = store.xp_by_day()
    goal = daily_goal(store)
    heatmap = []
    for offset in range(days - 1, -1, -1):
        day = (today - timedelta(days=offset)).isoformat()
        heatmap.append({"day": day, "xp": by_day.get(day, 0)})
    attempts = store.finished_attempts()
    answered = [a for attempt in attempts for a in attempt["answers"].values()]
    minutes = sum(_minutes(a) for a in attempts)
    read = store.one("SELECT COUNT(*) AS n FROM events WHERE kind = 'lesson_read'") or {"n": 0}
    events = store.events(limit=limit, before=before)
    return {
        "heatmap": heatmap,
        "goal": goal,
        "stats": {
            "xp": sum(by_day.values()),
            "active_days": len(active_days(store)),
            "quizzes": len(attempts),
            "lessons_read": read["n"],
            "lessons_passed": (store.one("SELECT COUNT(*) AS n FROM lessons WHERE passed_at IS NOT NULL") or {"n": 0})["n"],
            "courses_completed": (store.one("SELECT COUNT(*) AS n FROM courses WHERE completed_at IS NOT NULL") or {"n": 0})["n"],
            "questions": len(answered),
            "accuracy": round(sum(a.get("score", 0) for a in answered) / len(answered), 3) if answered else None,
            "quiz_minutes": minutes,
            "goal_days": sum(1 for v in by_day.values() if v >= goal),
        },
        "streak": streak(store),
        "events": events,
        "next_before": events[-1]["id"] if len(events) == limit else None,
    }


def _minutes(attempt: dict[str, Any]) -> int:
    try:
        spent = datetime.fromisoformat(attempt["finished_at"]) - datetime.fromisoformat(attempt["started_at"])
    except (TypeError, ValueError):
        return 0
    return max(1, min(60, round(spent.total_seconds() / 60)))
