"""The daily review: spaced repetition over every question you've answered.

Each answered question gets a card in a box (the Leitner system the starter
course teaches). Get it right and it moves up a box and comes back later;
get it wrong (or half right) and it drops to box 0 and comes back tomorrow.
The daily review is the cards that are due, up to 10 at a time. When more
are due than fit, cards from your weak spots (app/insights.py) go first.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from app.db import Store, local_day, now_iso

# Days until a card in each box comes back.
INTERVALS = [1, 3, 7, 14, 30, 60]
REVIEW_SIZE = 10


def key(lesson_id: str, qid: str) -> str:
    return f"{lesson_id}:{qid}"


def record(store: Store, lesson: dict[str, Any], qid: str, verdict: str, today: str | None = None) -> dict[str, Any]:
    """File one answer: move the card up a box, or back to box 0."""
    today = today or local_day()
    k = key(lesson["id"], qid)
    card = store.one("SELECT * FROM reviews WHERE key = ?", k)
    if verdict == "correct":
        box = min(len(INTERVALS) - 1, (card["box"] + 1) if card else 1)
        lapses = card["lapses"] if card else 0
    else:
        box = 0
        lapses = (card["lapses"] if card else 0) + 1
    due = (date.fromisoformat(today) + timedelta(days=INTERVALS[box])).isoformat()
    store.run(
        "INSERT INTO reviews (key, lesson_id, course_id, qid, box, due, seen, lapses, updated_at) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)"
        " ON CONFLICT(key) DO UPDATE SET box = excluded.box, due = excluded.due, seen = reviews.seen + 1,"
        " lapses = excluded.lapses, updated_at = excluded.updated_at",
        k, lesson["id"], lesson["course_id"], qid, box, due, lapses, now_iso(),
    )
    return {"box": box, "due": due}


def due_cards(store: Store, today: str | None = None, limit: int | None = REVIEW_SIZE) -> list[dict[str, Any]]:
    from app.insights import weak_lessons

    today = today or local_day()
    sql = ("SELECT r.* FROM reviews r JOIN lessons l ON l.id = r.lesson_id JOIN courses c ON c.id = r.course_id"
           " WHERE r.due <= ? AND l.status = 'ready' AND c.archived = 0 ORDER BY r.due, r.box, r.updated_at")
    cards = store.all(sql, today)
    if limit is None or len(cards) <= limit:
        return cards
    weak = weak_lessons(store)
    return sorted(cards, key=lambda c: c["lesson_id"] not in weak)[:limit]  # stable: weak first, then oldest due


def status(store: Store, today: str | None = None) -> dict[str, Any]:
    today = today or local_day()
    due = len(due_cards(store, today, limit=None))
    upcoming = store.one(
        "SELECT MIN(r.due) AS next FROM reviews r JOIN courses c ON c.id = r.course_id WHERE r.due > ? AND c.archived = 0", today)
    boxes = {r["box"]: r["n"] for r in store.all("SELECT box, COUNT(*) AS n FROM reviews GROUP BY box")}
    done_today = store.one("SELECT COUNT(*) AS n FROM events WHERE kind = 'review_finished' AND day = ?", today) or {"n": 0}
    return {
        "due": due,
        "next_due": (upcoming or {}).get("next"),
        "cards": sum(boxes.values()),
        "boxes": [boxes.get(i, 0) for i in range(len(INTERVALS))],
        "intervals": INTERVALS,
        "done_today": done_today["n"] > 0,
    }
