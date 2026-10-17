"""1.1: fresh retakes, the daily review, streak rules and freezes, final exams,
Siris links, photos, usage and cost, notifications, backups and course packs."""

from __future__ import annotations

import asyncio
import json
from datetime import date, datetime, timedelta

import httpx

from app import coursepacks, jobs, llm, photos, progress, push, siris, spaced
from app.db import get_store, local_day
from tests.conftest import right_answer, wait_for, wrong_answer


def _sample(client):
    course = client.get("/api/courses").json()[0]
    detail = client.get(f"/api/courses/{course['id']}").json()
    return course["id"], [l["id"] for s in detail["sections"] for l in s["lessons"]]


def _take(client, start_url, right=True):
    started = client.post(start_url).json()
    for q in started["questions"]:
        body = (right_answer if right else wrong_answer)(get_store(), started["attempt_id"], q)
        assert client.post(f"/api/attempts/{started['attempt_id']}/answer", json=body).status_code == 200
    return started, client.post(f"/api/attempts/{started['attempt_id']}/finish").json()


def _passed_day(store, day):
    store.insert("events", {"ts": f"{day}T01:00:00+00:00", "day": day, "kind": "quiz_finished", "xp": 10, "detail": {"passed": True}})


# -- retakes ---------------------------------------------------------------------


def test_retake_gets_fresh_questions(client, fake_llm):
    _, (lesson_id, _) = _sample(client)
    first, _ = _take(client, f"/api/lessons/{lesson_id}/attempts")
    # The first quiz starts writing a fresh set in the background.
    wait_for(lambda: len(get_store().lesson(lesson_id)["content"]["questions"]) == 20)
    from app import generator
    wait_for(lambda: not generator._tasks)
    lesson = client.get(f"/api/lessons/{lesson_id}").json()
    assert lesson["content"]["pool_size"] == 20 and lesson["content"]["unseen"] == 10
    second = client.post(f"/api/lessons/{lesson_id}/attempts").json()
    assert second["fresh"]
    assert not {q["id"] for q in first["questions"]} & {q["id"] for q in second["questions"]}
    assert all(q["prompt"].startswith("Fresh") for q in second["questions"])
    # Each quiz starts the next fresh set, so retakes keep getting new questions.
    assert sum(1 for c in fake_llm.calls if c["meta"].get("purpose") == "questions") >= 1


def test_retake_without_a_model_shuffles_seen_questions(client):
    llm.set_llm(None)
    _, (lesson_id, _) = _sample(client)
    _take(client, f"/api/lessons/{lesson_id}/attempts")
    started, done = _take(client, f"/api/lessons/{lesson_id}/attempts")
    assert not started["fresh"] and done["score"] == 1  # answers map back through the shuffled options


# -- the daily review ------------------------------------------------------------


def test_daily_review(client, fake_llm):
    store = get_store()
    _, (lesson_id, _) = _sample(client)
    fake_llm.verdict = "incorrect"
    _take(client, f"/api/lessons/{lesson_id}/attempts", right=False)
    assert client.post("/api/review").status_code == 409  # nothing due until tomorrow
    store.run("UPDATE reviews SET due = ?", local_day())
    status = client.get("/api/review").json()
    assert status["due"] == 10 and status["boxes"][0] == 10
    assert client.get("/api/summary").json()["review"]["due"] == 10
    fake_llm.verdict = "correct"
    started, done = _take(client, "/api/review")
    assert started["kind"] == "review" and len(started["questions"]) == 10
    assert done["kind"] == "review" and done["xp"] == 10 * 5 + 10
    assert done["streak"]["today_done"]  # a review counts for the streak
    assert client.get("/api/review").json() | {"boxes": None} == client.get("/api/review").json() | {"boxes": None}
    after = spaced.status(store)
    assert after["due"] == 0 and after["boxes"][1] == 10
    assert any(a["id"] == "first-review" for a in done["achievements"])


def test_review_intervals_grow():
    from app.db import reset_store

    store = reset_store(get_store().path.parent / "spaced.db")
    lesson = {"id": "l1", "course_id": "c1"}
    day = "2026-10-01"
    assert spaced.record(store, lesson, "q1", "correct", day) == {"box": 1, "due": "2026-10-04"}
    assert spaced.record(store, lesson, "q1", "correct", day)["due"] == "2026-10-08"
    assert spaced.record(store, lesson, "q1", "incorrect", day) == {"box": 0, "due": "2026-10-02"}


# -- streak rules and freezes ------------------------------------------------------


def test_freezes_cover_a_missed_day(store):
    start = date(2026, 9, 1)
    days = [start + timedelta(days=i) for i in range(7)] + [start + timedelta(days=8)]  # day 8 (index 7) missed
    for d in days:
        _passed_day(store, d.isoformat())
    last = days[-1]
    s = progress.streak(store, last.isoformat())
    assert s["current"] == 8 and s["freezes"] == 0 and s["frozen_days"] == [(start + timedelta(days=7)).isoformat()]
    # Two days later with no freeze left: gone.
    assert progress.streak(store, (last + timedelta(days=2)).isoformat())["current"] == 0


def test_a_freeze_holds_the_streak_while_you_catch_up(store):
    start = date(2026, 9, 1)
    for i in range(7):
        _passed_day(store, (start + timedelta(days=i)).isoformat())
    s = progress.streak(store, (start + timedelta(days=8)).isoformat())  # missed yesterday
    assert s["current"] == 7 and s["at_risk"] and s["freeze_in_use"] and s["freezes"] == 0


# -- final exam and certificate -----------------------------------------------------


def test_final_exam_and_certificate(client, fake_llm):
    llm.set_llm(None)  # no fresh sets: the exam draws from the original 20 questions
    course_id, lessons = _sample(client)
    assert client.post(f"/api/courses/{course_id}/exam").status_code == 409
    for lesson_id in lessons:
        _take(client, f"/api/lessons/{lesson_id}/attempts")
    exam = client.get(f"/api/courses/{course_id}").json()["exam"]
    assert exam["unlocked"] and exam["questions"] == 20
    assert client.get(f"/api/courses/{course_id}/certificate").status_code == 404
    started, done = _take(client, f"/api/courses/{course_id}/exam")
    assert started["kind"] == "exam" and len(started["questions"]) == 20
    assert done["passed"] and done["first_pass"] and done["xp"] == 150
    assert any(a["id"] == "certified" for a in done["achievements"])
    cert = client.get(f"/api/courses/{course_id}/certificate").json()
    assert cert["name"] == "Brad" and cert["course"] == "How to learn anything faster" and cert["score"] == 1
    assert cert["reference"].startswith("SL-")
    review = client.get(f"/api/attempts/{started['attempt_id']}").json()
    assert review["kind"] == "exam" and all(q["result"]["verdict"] == "correct" for q in review["questions"])


# -- Siris -----------------------------------------------------------------------


class FakeSirisAI:
    def __init__(self):
        self.captured = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.headers.get("authorization") != "Bearer ai-key":
            return httpx.Response(401)
        if request.url.path == "/siris/brain/capture":
            self.captured.append(json.loads(request.content))
            return httpx.Response(200, json={"action": "captured", "title": "x"})
        if request.url.path == "/siris/brain/insights":
            return httpx.Response(200, json={"topics": [{"tag": "home-assistant", "notes": 9}, {"tag": "sirislearn", "notes": 20},
                                                        {"tag": "learning", "notes": 3}, {"tag": "pump-curves", "notes": 4}]})
        return httpx.Response(404)


def test_passing_a_lesson_saves_it_to_the_second_brain(client, monkeypatch):
    fake = FakeSirisAI()
    monkeypatch.setattr(siris, "transport", httpx.MockTransport(fake))
    monkeypatch.setenv("SIRISAI_URL", "http://ai:8000")
    monkeypatch.setenv("SIRISAI_API_KEY", "ai-key")
    monkeypatch.setenv("SIRISLEARN_PUBLIC_URL", "https://learn.local")
    _, (lesson_id, _) = _sample(client)
    _, done = _take(client, f"/api/lessons/{lesson_id}/attempts")
    assert done["brain"] == "saving"
    wait_for(lambda: get_store().lesson(lesson_id)["brain_saved_at"])
    [note] = fake.captured
    assert note["text"].startswith("Why we forget") and "Key points:" in note["text"]
    assert note["url"] == f"https://learn.local/lesson/{lesson_id}" and "sirislearn" in note["tags"]
    # Once only, and the setting turns it off.
    _take(client, f"/api/lessons/{lesson_id}/attempts")
    assert len(fake.captured) == 1
    assert client.put("/api/settings", json={"brain_capture": False}).json()["brain"]["enabled"] is False


def test_suggestions_come_from_the_second_brain(client, monkeypatch):
    assert client.get("/api/suggestions").json()["source"] == "ideas"
    monkeypatch.setattr(siris, "transport", httpx.MockTransport(FakeSirisAI()))
    monkeypatch.setenv("SIRISAI_URL", "http://ai:8000")
    monkeypatch.setenv("SIRISAI_API_KEY", "ai-key")
    ideas = client.get("/api/suggestions").json()
    assert ideas == {"source": "brain", "ideas": ["Home assistant", "Pump curves"]}


def test_ask_siris_about_a_lesson(client, monkeypatch):
    _, (lesson_id, _) = _sample(client)
    monkeypatch.setenv("SIRISOS_PUBLIC_URL", "https://os.local")
    out = client.post(f"/api/lessons/{lesson_id}/ask", json={"question": "Why does spacing work?"}).json()
    assert out == {"answer": "Think of it like this.", "sirisos_assistant": "https://os.local/assistant"}
    llm.set_llm(None)
    assert client.post(f"/api/lessons/{lesson_id}/ask", json={"question": "Why?"}).status_code == 503


# -- course areas and tags -----------------------------------------------------------


def test_planned_course_gets_an_area_and_clean_tags(client):
    created = client.post("/api/courses", json={"topic": "heat pumps"}).json()
    course = wait_for(lambda: (c := client.get(f"/api/courses/{created['id']}").json())["status"] == "ready" and c)
    assert course["area"] == "engineering" and course["tags"] == ["heat-pumps", "hvac"]


# -- photos ----------------------------------------------------------------------------


def test_wikimedia_photo_with_credit(monkeypatch):
    def commons(request: httpx.Request) -> httpx.Response:
        assert "filetype:bitmap centrifugal pump" in request.url.params["gsrsearch"]
        return httpx.Response(200, json={"query": {"pages": {
            "1": {"index": 1, "title": "File:Logo.png", "imageinfo": [{"thumburl": "https://u/logo.png", "width": 1200,
                                                                     "extmetadata": {"LicenseShortName": {"value": "Copyrighted"}}}]},
            "2": {"index": 2, "title": "File:Pump.jpg", "imageinfo": [{"thumburl": "https://upload.wikimedia.org/pump.jpg", "width": 1200,
                                                                     "descriptionurl": "https://commons.wikimedia.org/wiki/File:Pump.jpg",
                                                                     "extmetadata": {"LicenseShortName": {"value": "CC BY-SA 4.0"},
                                                                                     "Artist": {"value": "<a href='x'>Jane Doe</a>"}}}]},
        }}})

    monkeypatch.setattr(photos, "transport", httpx.MockTransport(commons))
    monkeypatch.setenv("SIRISLEARN_PHOTOS", "true")
    photo = asyncio.run(photos.find("centrifugal pump"))
    assert photo == {"url": "https://upload.wikimedia.org/pump.jpg", "page": "https://commons.wikimedia.org/wiki/File:Pump.jpg",
                     "title": "Pump", "author": "Jane Doe", "licence": "CC BY-SA 4.0", "query": "centrifugal pump"}
    monkeypatch.setenv("SIRISLEARN_PHOTOS", "false")
    assert asyncio.run(photos.find("centrifugal pump")) is None


# -- usage and cost ----------------------------------------------------------------------


def test_usage_and_cost(client):
    assert round(llm.cost("claude-opus-5-5", 1_000_000, 100_000, 2_000_000, 0), 4) == 4 + 2 + 0.4
    llm.record_usage("claude-opus-5-5", {"purpose": "lesson", "course_id": "zzz"}, 10_000, 8_000, 20_000, 2_000)
    usage = client.get("/api/settings").json()["usage"]
    assert usage["calls"] == 1 and usage["cost"] > 0 and usage["by_purpose"][0]["purpose"] == "lesson"
    assert usage["by_course"][0]["title"] == "Deleted course"


# -- notifications and backups --------------------------------------------------------------


def test_push_subscriptions(client):
    assert len(client.get("/api/push/key").json()["key"]) > 80
    bad = client.post("/api/push/subscribe", json={"endpoint": "http://x", "keys": {}})
    assert bad.status_code == 422
    sub = {"endpoint": "https://push.example/abc", "keys": {"p256dh": "k", "auth": "a"}}
    assert client.post("/api/push/subscribe", json=sub).json()["subscriptions"] == 1
    assert client.post("/api/push/unsubscribe", json={"endpoint": sub["endpoint"]}).json()["subscriptions"] == 0


def test_jobs_send_reminders_once_and_back_up(store, monkeypatch, tmp_path):
    sent = []
    monkeypatch.setattr(push, "sender", lambda sub, payload: sent.append(payload) or (410 if "gone" in sub["endpoint"] else 201))
    push.subscribe(store, {"endpoint": "https://push.example/phone", "keys": {"p256dh": "k", "auth": "a"}})
    push.subscribe(store, {"endpoint": "https://push.example/gone", "keys": {"p256dh": "k", "auth": "a"}})
    from app import config

    today = local_day()
    _passed_day(store, (date.fromisoformat(today) - timedelta(days=1)).isoformat())  # streak at risk today
    store.insert("reviews", {"key": "l:q", "lesson_id": "l", "course_id": "c", "qid": "q", "box": 0, "due": today, "updated_at": "x"})
    evening = datetime.fromisoformat(f"{today}T20:00:00").replace(tzinfo=config.timezone())
    ran = asyncio.run(jobs.tick(store, evening))
    assert "backup" in ran and "streak" in ran
    assert sent[0]["title"] == "Your 1-day streak ends at midnight"
    assert (store.one("SELECT COUNT(*) AS n FROM push_subscriptions") or {})["n"] == 1  # the gone one is removed
    assert list((tmp_path / "backups").glob("sirislearn-*.db"))
    assert asyncio.run(jobs.tick(store, evening)) == []  # once a day


def test_backups_are_pruned(store, monkeypatch, tmp_path):
    monkeypatch.setenv("SIRISLEARN_BACKUP_DAYS", "2")
    for day in ("2026-10-01", "2026-10-02", "2026-10-03"):
        jobs.backup(store, day)
    assert sorted(p.name for p in (tmp_path / "backups").glob("*.db")) == ["sirislearn-2026-10-02.db", "sirislearn-2026-10-03.db"]


# -- course packs -------------------------------------------------------------------------------


def test_course_pack_installs_once(store, monkeypatch):
    from app.sample import LESSON_1

    lesson = {**LESSON_1, "questions": LESSON_1["questions"] * 2}  # a 20-question pool survives
    pack = {"id": "test-pack", "version": 1, "topic": "Testing", "title": "Testing 101", "summary": "s", "icon": "code",
            "level": "beginner", "length": "short", "area": "technology", "tags": ["testing"],
            "sections": [{"title": "One", "summary": "s", "lessons": [{"title": "L1", "summary": "s", "lesson": lesson}]}]}
    monkeypatch.setattr(coursepacks, "available", lambda: [pack])
    monkeypatch.setenv("SIRISLEARN_SEED_PACKS", "true")
    assert coursepacks.seed(store) == ["test-pack"]
    assert coursepacks.seed(store) == []
    [course] = [c for c in store.courses() if c["pack"] == "test-pack"]
    [row] = store.lessons(course["id"])
    assert row["status"] == "ready" and len(row["content"]["questions"]) == 20 and course["tags"] == ["testing"]


def test_history_reports_the_server_day(client):
    assert client.get("/api/history").json()["today"] == local_day()
