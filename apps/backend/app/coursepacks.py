"""Loads the built-in course packs (app/packs/*.py) into the library, once
each. A pack is a complete course: plan, lessons and question pools, so it
works without a model. SIRISLEARN_SEED_PACKS=false skips them; deleting a
pack course keeps it deleted. When a pack's `version` goes up, the course
already in the library is upgraded in place: each lesson's content is
replaced but its id, progress and review cards stay. Questions keep their
ids as long as new ones are only added at the end of a lesson's list.

A pack module defines PACK:

    PACK = {
        "id": "docker-beginner", "version": 1,
        "topic": ..., "title": ..., "summary": ..., "icon": ..., "level": ...,
        "length": ..., "area": ..., "tags": [...],
        "sections": [{"title": ..., "summary": ..., "lessons": [
            {"title": ..., "summary": ..., "lesson": {<lesson content as the writer returns it>}},
        ]}],
    }

`mcq()`, `open_q()`, `scenario()` and `calc()` below keep the question lists short to write.
"""

from __future__ import annotations

import copy
import hashlib
import importlib
import random
import logging
import pkgutil
from typing import Any

from app import config
from app.db import Store, new_id, now_iso
from app.generator import clean_lesson

logger = logging.getLogger(__name__)


def mcq(prompt: str, options: list[str], answer: int, explanation: str, svg: str = "", alt: str = "") -> dict[str, Any]:
    return {"kind": "mcq", "prompt": prompt, "options": options, "answer_index": answer, "explanation": explanation,
            "svg": svg, "image_alt": alt, "model_answer": "", "key_points": []}


def open_q(prompt: str, model_answer: str, key_points: list[str], explanation: str, svg: str = "", alt: str = "") -> dict[str, Any]:
    return {"kind": "open", "prompt": prompt, "options": [], "answer_index": -1, "model_answer": model_answer,
            "key_points": key_points, "explanation": explanation, "svg": svg, "image_alt": alt}


def scenario(prompt: str, model_answer: str, rubric: list[str], explanation: str, svg: str = "", alt: str = "") -> dict[str, Any]:
    """A short case to respond to, marked against the rubric (what a good response does)."""
    return {**open_q(prompt, model_answer, rubric, explanation, svg, alt), "kind": "scenario"}


def calc(prompt: str, answer: float, unit: str, working: str, explanation: str = "", tolerance: float = 2.0,
         svg: str = "", alt: str = "") -> dict[str, Any]:
    """A numeric answer, right within `tolerance` percent, with the worked solution."""
    return {"kind": "calc", "prompt": prompt, "options": [], "answer_index": -1, "model_answer": "", "key_points": [],
            "answer_value": answer, "tolerance": tolerance, "unit": unit, "working": working, "explanation": explanation,
            "svg": svg, "image_alt": alt}


def balanced(lesson: dict[str, Any], seed: str) -> dict[str, Any]:
    """Spread the right answers evenly over the option positions (the same
    way every time), so it isn't always B."""
    out = copy.deepcopy(lesson)
    rng = random.Random(hashlib.sha256(f"{seed}:{lesson.get('title', '')}".encode()).hexdigest())
    slots: list[int] = []
    for q in out.get("questions") or []:
        if q.get("kind") != "mcq":
            continue
        n = len(q["options"])
        if not slots:
            slots = list(range(n))
            rng.shuffle(slots)
        target = slots.pop() % n
        right = q["options"][q["answer_index"]]
        others = [o for i, o in enumerate(q["options"]) if i != q["answer_index"]]
        rng.shuffle(others)
        others.insert(target, right)
        q["options"], q["answer_index"] = others, target
    return out


def available() -> list[dict[str, Any]]:
    import app.packs as package

    out = []
    for info in sorted(pkgutil.iter_modules(package.__path__), key=lambda m: m.name):
        module = importlib.import_module(f"app.packs.{info.name}")
        pack = getattr(module, "PACK", None)
        if isinstance(pack, dict):
            out.append(pack)
    return out


def install(store: Store, pack: dict[str, Any]) -> str:
    now = now_iso()
    course_id = new_id()
    store.insert("courses", {
        "id": course_id, "topic": pack["topic"], "title": pack["title"], "summary": pack["summary"], "icon": pack["icon"],
        "level": pack["level"], "length": pack["length"], "area": pack.get("area", "other"), "tags": pack.get("tags", []),
        "sections": [{"title": s["title"], "summary": s["summary"]} for s in pack["sections"]],
        "pack": pack["id"], "status": "ready", "created_at": now, "updated_at": now,
    })
    rows, position = [], 0
    for s_idx, section in enumerate(pack["sections"]):
        for lesson in section["lessons"]:
            rows.append({"id": new_id(), "course_id": course_id, "section_idx": s_idx, "position": position,
                         "title": lesson["title"], "summary": lesson["summary"], "status": "ready",
                         "content": clean_lesson(balanced(lesson["lesson"], pack["id"]), max_questions=None), "generated_at": now})
            position += 1
    store.replace_lessons(course_id, rows)
    return course_id


def upgrade(store: Store, pack: dict[str, Any]) -> bool:
    """Bring an installed pack course up to the pack's current content."""
    course = store.one("SELECT * FROM courses WHERE pack = ? ORDER BY created_at LIMIT 1", pack["id"])
    if course is None:
        return False
    lessons = store.lessons(course["id"])
    written = [l for s in pack["sections"] for l in s["lessons"]]
    if len(lessons) != len(written):
        logger.warning("Course pack %s changed shape; leaving the installed copy as it is", pack["id"])
        return False
    for row, entry in zip(lessons, written):
        if (row.get("content") or {}).get("refreshed_at"):
            continue  # rewritten from the news since; keep that version
        content = clean_lesson(balanced(entry["lesson"], pack["id"]), max_questions=None)
        if (row.get("content") or {}).get("photo") is not None:
            content["photo"] = row["content"]["photo"]
        store.update("lessons", row["id"], content=content, title=entry["title"], summary=entry["summary"])
    store.update("courses", course["id"], summary=pack["summary"], tags=pack.get("tags", []))
    return True


def seed(store: Store) -> list[str]:
    if config.env("SIRISLEARN_SEED_PACKS", "true").lower() in ("0", "false", "no"):
        return []
    added = []
    for pack in available():
        key = f"pack:{pack['id']}"
        installed = store.setting(key)
        if installed:
            if int(installed or 1) < int(pack.get("version", 1)):
                try:
                    if upgrade(store, pack):
                        logger.info("Upgraded course pack %s to version %s", pack["id"], pack.get("version"))
                except Exception:
                    logger.exception("Couldn't upgrade course pack %s", pack["id"])
                    continue
                store.set_setting(key, str(pack.get("version", 1)))
            continue
        try:
            install(store, pack)
        except Exception:
            logger.exception("Couldn't add course pack %s", pack.get("id"))
            continue
        store.set_setting(key, str(pack.get("version", 1)))
        added.append(pack["id"])
    if added:
        logger.info("Added course packs: %s", ", ".join(added))
    return added
