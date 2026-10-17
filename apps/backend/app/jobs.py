"""Background jobs, checked every few minutes while the app runs:

- **Streak reminder** at SIRISLEARN_REMINDER_HOUR (default 7 pm local): a
  push notification if your streak ends at midnight.
- **Review reminder** at SIRISLEARN_REVIEW_HOUR (default 8 am): how many
  cards are due today.
- **Backup**: once a day, a consistent copy of the database to
  data/backups/sirislearn-YYYY-MM-DD.db, keeping the last
  SIRISLEARN_BACKUP_DAYS (default 14).

Each job remembers the day it last ran (settings), so a restart never sends
twice.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from app import config, push, spaced
from app.db import Store, get_store, local_day
from app.progress import streak

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = 300


def backup_days() -> int:
    return max(1, int(config.env("SIRISLEARN_BACKUP_DAYS", "14")))


def backup(store: Store, today: str) -> str | None:
    folder = config.data_dir() / "backups"
    target = folder / f"sirislearn-{today}.db"
    if target.exists():
        return None
    store.backup(target)
    for old in sorted(folder.glob("sirislearn-*.db"))[:-backup_days()]:
        old.unlink(missing_ok=True)
    return str(target)


async def tick(store: Store, now: datetime | None = None) -> list[str]:
    """Run whatever is due; returns what ran (for logs and tests)."""
    now = now or datetime.now(config.timezone())
    today = local_day(now.isoformat())
    ran: list[str] = []

    if store.setting("job_backup") != today:
        backup(store, today)
        store.set_setting("job_backup", today)
        ran.append("backup")

    if now.hour >= push.reminder_hour() and store.setting("job_streak") != today:
        store.set_setting("job_streak", today)
        s = streak(store, today)
        if s["at_risk"]:
            days = s["current"]
            await push.send(store, f"Your {days}-day streak ends at midnight",
                            "One passed quiz or your daily review keeps it going.", url="/", tag="streak")
            ran.append("streak")

    if now.hour >= push.review_hour() and store.setting("job_review") != today:
        store.set_setting("job_review", today)
        due = spaced.status(store, today)["due"]
        if due:
            await push.send(store, f"{due} card{'s' if due != 1 else ''} to review",
                            "A few minutes of review keeps what you've learned.", url="/review", tag="review")
            ran.append("review")
    return ran


async def run_forever() -> None:
    while True:
        try:
            ran = await tick(get_store())
            if ran:
                logger.info("Jobs ran: %s", ", ".join(ran))
        except Exception:
            logger.exception("Background jobs failed")
        await asyncio.sleep(INTERVAL_SECONDS)
