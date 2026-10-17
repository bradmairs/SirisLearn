"""Every test gets a fresh database and a fake model (no network)."""

from __future__ import annotations

import copy
import time
from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient

from app import db, llm
from app.sample import LESSON_1


def truth(store, question_ref: str) -> dict[str, Any]:
    """The stored question behind a quiz's question id."""
    lesson_id, qid = question_ref.split(":")
    return next(q for q in store.lesson(lesson_id)["content"]["questions"] if q["id"] == qid)


def right_answer(store, attempt_id: str, q: dict[str, Any]) -> dict[str, Any]:
    """An answer body that's correct, honouring the attempt's option order."""
    t = truth(store, q["id"])
    if q["kind"] != "mcq":
        return {"question_id": q["id"], "text": t["model_answer"]}
    return {"question_id": q["id"], "choice": q["options"].index(t["options"][t["answer_index"]])}


def wrong_answer(store, attempt_id: str, q: dict[str, Any]) -> dict[str, Any]:
    if q["kind"] != "mcq":
        return {"question_id": q["id"], "text": "no idea"}
    t = truth(store, q["id"])
    right = q["options"].index(t["options"][t["answer_index"]])
    return {"question_id": q["id"], "choice": (right + 1) % len(q["options"])}


class FakeLLM:
    """Answers each kind of request by the schema it's asked for."""

    name = "fake"
    model = "fake-model"

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.fail_lessons = False
        self.verdict = "correct"

    async def json(self, *, system, context, prompt, schema, effort="medium", max_tokens=32000, meta=None):
        self.calls.append({"system": system, "context": context, "prompt": prompt, "effort": effort, "meta": meta or {}})
        props = schema["properties"]
        if "answer" in props:
            return {"answer": "Think of it like this."}
        if list(props) == ["questions"]:
            fresh = copy.deepcopy(LESSON_1["questions"])
            for i, q in enumerate(fresh):
                q["prompt"] = f"Fresh {i}: {q['prompt']}"
            return {"questions": fresh}
        if "sections" in props:
            return {
                "title": "Heat pumps", "summary": "How heat pumps work.", "icon": "zap", "area": "engineering",
                "tags": ["Heat Pumps", "hvac", "hvac"],
                "sections": [
                    {"title": "Basics", "summary": "s", "lessons": [{"title": "Moving heat", "summary": "a"}, {"title": "Refrigerants", "summary": "b"}]},
                    {"title": "In practice", "summary": "s", "lessons": [{"title": "Sizing", "summary": "c"}]},
                ],
            }
        if "questions" in props:
            if self.fail_lessons:
                return {"title": "x", "minutes": 5, "body": "too short", "key_points": [], "figure_svg": "", "figure_caption": "", "questions": []}
            lesson = copy.deepcopy(LESSON_1)
            lesson["figure_svg"] = '<svg viewBox="0 0 10 10"><script>alert(1)</script><rect onclick="x()" width="5" height="5"/></svg>'
            return lesson
        return {"verdict": self.verdict, "feedback": "Nice."}


@pytest.fixture()
def fake_llm():
    fake = FakeLLM()
    llm.set_llm(fake)
    yield fake
    llm.set_llm(None)


@pytest.fixture()
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("SIRISLEARN_DATA_PATH", str(tmp_path))
    monkeypatch.setenv("SIRISLEARN_HUB_KEY", "hub-key")
    monkeypatch.setenv("SIRISLEARN_ADMIN_PASSWORD", "pw")
    monkeypatch.setenv("SIRISLEARN_JOBS", "false")
    monkeypatch.setenv("SIRISLEARN_PHOTOS", "false")
    monkeypatch.setenv("SIRISLEARN_SEED_PACKS", "false")
    return db.reset_store(tmp_path / "test.db")


@pytest.fixture()
def client(store, fake_llm):
    from app.main import app

    with TestClient(app) as c:
        token = c.post("/api/auth/login", json={"username": "brad", "password": "pw"}).json()["access_token"]
        c.headers["Authorization"] = f"Bearer {token}"
        yield c


def wait_for(check: Callable[[], Any], timeout: float = 5.0) -> Any:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = check()
        if value:
            return value
        time.sleep(0.02)
    raise AssertionError("timed out waiting")
