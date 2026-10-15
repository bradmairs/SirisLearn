"""SQLite storage: courses, lessons, quiz attempts, the learning history
(events), unlocked achievements and settings. One file, data/sirislearn.db.

Courses keep their section list in `outline`; lessons are rows of their own
so each can be written, regenerated and scored on its own. History events
copy the course and lesson titles, so the history survives deleting a course.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from app import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS courses (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    summary TEXT NOT NULL DEFAULT '',
    icon TEXT NOT NULL DEFAULT 'book',
    level TEXT NOT NULL DEFAULT 'beginner',
    length TEXT NOT NULL DEFAULT 'standard',
    notes TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL,
    error TEXT NOT NULL DEFAULT '',
    sections TEXT NOT NULL DEFAULT '[]',
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT
);
CREATE TABLE IF NOT EXISTS lessons (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    section_idx INTEGER NOT NULL,
    position INTEGER NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    error TEXT NOT NULL DEFAULT '',
    content TEXT,
    generated_at TEXT,
    read_at TEXT,
    best_score REAL,
    passed_at TEXT
);
CREATE INDEX IF NOT EXISTS lessons_course ON lessons(course_id, position);
CREATE TABLE IF NOT EXISTS attempts (
    id TEXT PRIMARY KEY,
    lesson_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    correct REAL NOT NULL DEFAULT 0,
    total INTEGER NOT NULL DEFAULT 0,
    score REAL,
    xp INTEGER NOT NULL DEFAULT 0,
    answers TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS attempts_lesson ON attempts(lesson_id);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    day TEXT NOT NULL,
    kind TEXT NOT NULL,
    course_id TEXT,
    lesson_id TEXT,
    title TEXT NOT NULL DEFAULT '',
    course_title TEXT NOT NULL DEFAULT '',
    xp INTEGER NOT NULL DEFAULT 0,
    detail TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS events_day ON events(day);
CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY,
    unlocked_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

JSON_FIELDS = {"sections", "content", "answers", "detail"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id() -> str:
    return uuid.uuid4().hex[:12]


def local_day(ts: str | None = None) -> str:
    moment = datetime.fromisoformat(ts) if ts else datetime.now(timezone.utc)
    return moment.astimezone(config.timezone()).date().isoformat()


def _row(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    out = dict(row)
    for key in JSON_FIELDS & out.keys():
        if isinstance(out[key], str):
            out[key] = json.loads(out[key])
    return out


def _encode(value: Any) -> Any:
    return json.dumps(value) if isinstance(value, (dict, list)) else value


class Store:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.RLock()
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.executescript(SCHEMA)

    # -- low level -----------------------------------------------------------

    def one(self, sql: str, *args: Any) -> dict[str, Any] | None:
        with self.lock:
            return _row(self.conn.execute(sql, args).fetchone())

    def all(self, sql: str, *args: Any) -> list[dict[str, Any]]:
        with self.lock:
            return [_row(r) for r in self.conn.execute(sql, args).fetchall()]  # type: ignore[misc]

    def run(self, sql: str, *args: Any) -> int:
        with self.lock, self.conn:
            return self.conn.execute(sql, [_encode(a) for a in args]).rowcount

    def insert(self, table: str, row: dict[str, Any]) -> None:
        cols = ", ".join(row)
        marks = ", ".join("?" for _ in row)
        self.run(f"INSERT INTO {table} ({cols}) VALUES ({marks})", *row.values())

    def update(self, table: str, key: str, **fields: Any) -> None:
        sets = ", ".join(f"{k} = ?" for k in fields)
        self.run(f"UPDATE {table} SET {sets} WHERE id = ?", *fields.values(), key)

    # -- courses and lessons -------------------------------------------------

    def course(self, course_id: str) -> dict[str, Any] | None:
        return self.one("SELECT * FROM courses WHERE id = ?", course_id)

    def courses(self) -> list[dict[str, Any]]:
        return self.all("SELECT * FROM courses ORDER BY updated_at DESC")

    def lesson(self, lesson_id: str) -> dict[str, Any] | None:
        return self.one("SELECT * FROM lessons WHERE id = ?", lesson_id)

    def lessons(self, course_id: str) -> list[dict[str, Any]]:
        return self.all("SELECT * FROM lessons WHERE course_id = ? ORDER BY position", course_id)

    def touch_course(self, course_id: str) -> None:
        self.run("UPDATE courses SET updated_at = ? WHERE id = ?", now_iso(), course_id)

    def replace_lessons(self, course_id: str, lessons: Iterable[dict[str, Any]]) -> None:
        with self.lock, self.conn:
            self.conn.execute("DELETE FROM lessons WHERE course_id = ?", (course_id,))
            for row in lessons:
                cols = ", ".join(row)
                self.conn.execute(
                    f"INSERT INTO lessons ({cols}) VALUES ({', '.join('?' for _ in row)})",
                    [_encode(v) for v in row.values()],
                )

    def delete_course(self, course_id: str) -> None:
        with self.lock, self.conn:
            self.conn.execute("DELETE FROM attempts WHERE course_id = ?", (course_id,))
            self.conn.execute("DELETE FROM lessons WHERE course_id = ?", (course_id,))
            self.conn.execute("DELETE FROM courses WHERE id = ?", (course_id,))

    # -- attempts --------------------------------------------------------------

    def attempt(self, attempt_id: str) -> dict[str, Any] | None:
        return self.one("SELECT * FROM attempts WHERE id = ?", attempt_id)

    def finished_attempts(self) -> list[dict[str, Any]]:
        return self.all("SELECT * FROM attempts WHERE finished_at IS NOT NULL ORDER BY finished_at")

    # -- history ---------------------------------------------------------------

    def log(self, kind: str, *, title: str = "", course: dict[str, Any] | None = None,
            lesson_id: str | None = None, xp: int = 0, detail: dict[str, Any] | None = None,
            ts: str | None = None) -> None:
        ts = ts or now_iso()
        self.insert("events", {
            "ts": ts,
            "day": local_day(ts),
            "kind": kind,
            "course_id": course["id"] if course else None,
            "lesson_id": lesson_id,
            "title": title,
            "course_title": (course or {}).get("title") or (course or {}).get("topic") or "",
            "xp": xp,
            "detail": detail or {},
        })

    def events(self, kinds: Iterable[str] | None = None, limit: int = 1000, before: int | None = None) -> list[dict[str, Any]]:
        sql, args = "SELECT * FROM events WHERE 1 = 1", []
        if kinds:
            kinds = list(kinds)
            sql += f" AND kind IN ({', '.join('?' for _ in kinds)})"
            args += kinds
        if before:
            sql += " AND id < ?"
            args.append(before)
        sql += " ORDER BY id DESC LIMIT ?"
        args.append(limit)
        return self.all(sql, *args)

    def xp_by_day(self) -> dict[str, int]:
        return {r["day"]: r["xp"] for r in self.all("SELECT day, SUM(xp) AS xp FROM events GROUP BY day")}

    # -- achievements and settings ---------------------------------------------

    def unlocked(self) -> dict[str, str]:
        return {r["id"]: r["unlocked_at"] for r in self.all("SELECT * FROM achievements")}

    def unlock(self, achievement_id: str) -> None:
        self.run("INSERT OR IGNORE INTO achievements (id, unlocked_at) VALUES (?, ?)", achievement_id, now_iso())

    def setting(self, key: str, default: str = "") -> str:
        row = self.one("SELECT value FROM settings WHERE key = ?", key)
        return row["value"] if row else default

    def set_setting(self, key: str, value: str) -> None:
        self.run("INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value", key, value)


_store: Store | None = None


def get_store() -> Store:
    global _store
    if _store is None:
        _store = Store(config.data_dir() / "sirislearn.db")
    return _store


def reset_store(path: Path | None = None) -> Store:
    """Tests: a fresh database."""
    global _store
    _store = Store(path or config.data_dir() / "sirislearn.db")
    return _store
