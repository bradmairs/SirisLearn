"""1.2: every built-in course is complete and survives the same cleaning as a generated lesson."""

from __future__ import annotations

import pytest

from app import coursepacks, svg
from app.generator import clean_lesson

PACKS = coursepacks.available()
LESSONS = [(p["id"], l) for p in PACKS for s in p["sections"] for l in s["lessons"]]


def test_all_built_in_courses_ship():
    assert {p["id"] for p in PACKS} >= {f"{t}-{lvl}" for t in ("docker", "linux", "water")
                                        for lvl in ("beginner", "intermediate", "advanced")} | {"ai-general", "ai-use"}


@pytest.mark.parametrize("pack_id,entry", LESSONS, ids=[f"{p}:{l['title']}" for p, l in LESSONS])
def test_lesson_is_complete(pack_id, entry):
    raw = coursepacks.balanced(entry["lesson"], pack_id)
    content = clean_lesson(raw, max_questions=None)
    qs = content["questions"]
    assert len(qs) == len(raw["questions"]) >= 10
    assert sum(1 for q in qs if q["svg"]) >= 2
    assert sum(1 for q in qs if q["kind"] == "open") >= 3
    assert content["figure_svg"] and svg.sanitize(raw["figure_svg"])
    for q in raw["questions"]:
        if q["kind"] == "mcq":
            assert len(set(q["options"])) == len(q["options"]) and 0 <= q["answer_index"] < len(q["options"])
