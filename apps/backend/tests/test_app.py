"""The whole learning loop through the API, with a fake model."""

from __future__ import annotations

from datetime import date, timedelta

from app import achievements, progress, svg
from app.db import get_store
from tests.conftest import right_answer, wait_for, wrong_answer


def _course(client, course_id):
    return client.get(f"/api/courses/{course_id}").json()


def _create(client):
    created = client.post("/api/courses", json={"topic": "heat pumps", "level": "intermediate", "length": "short"})
    assert created.status_code == 201
    course_id = created.json()["id"]
    return wait_for(lambda: (c := _course(client, course_id))["status"] == "ready" and c)


def test_login_required(store, fake_llm):
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        assert c.get("/api/courses").status_code == 401
        assert c.post("/api/auth/login", json={"username": "brad", "password": "nope"}).status_code == 401
        assert c.get("/health").json()["status"] == "ok"


def test_sample_course_is_seeded_once(client):
    courses = client.get("/api/courses").json()
    assert [c["title"] for c in courses] == ["How to learn anything faster"]
    assert courses[0]["progress"]["lessons"] == 2
    from app import sample

    sample.seed(get_store())
    assert len(client.get("/api/courses").json()) == 1


def test_course_is_planned_then_lessons_written_on_open(client, fake_llm):
    course = _create(client)
    assert course["title"] == "Heat pumps" and course["icon"] == "zap"
    assert [len(s["lessons"]) for s in course["sections"]] == [2, 1]
    first, second = course["sections"][0]["lessons"]
    # The first lesson is written straight after planning.
    wait_for(lambda: client.get(f"/api/lessons/{first['id']}").json()["status"] == "ready")
    lesson = client.get(f"/api/lessons/{first['id']}").json()
    assert lesson["content"]["question_count"] == 10
    assert "questions" not in lesson["content"]
    assert "<script" not in lesson["content"]["figure_svg"] and "onclick" not in lesson["content"]["figure_svg"]
    assert lesson["number"] == 1 and lesson["of"] == 3 and lesson["next_id"] == second["id"]
    # Opening it writes the next one ahead.
    wait_for(lambda: client.get(f"/api/lessons/{second['id']}").json()["status"] == "ready")
    writer_calls = [c for c in fake_llm.calls if "Write Lesson" in c["prompt"]]
    assert "Lesson 1.2: Refrigerants" in writer_calls[0]["context"]
    assert "Write Lesson 1.1" in writer_calls[0]["prompt"]


def test_failed_lesson_can_be_retried(client, fake_llm):
    fake_llm.fail_lessons = True
    course = _create(client)
    first = course["sections"][0]["lessons"][0]["id"]
    lesson = wait_for(lambda: (l := client.get(f"/api/lessons/{first}").json())["status"] == "error" and l)
    assert "incomplete" in lesson["error"]
    fake_llm.fail_lessons = False
    client.post(f"/api/courses/{course['id']}/retry")
    wait_for(lambda: client.get(f"/api/lessons/{first}").json()["status"] == "ready")


def test_no_model_marks_course_failed(client):
    from app import llm

    llm.set_llm(None)
    created = client.post("/api/courses", json={"topic": "knots"}).json()
    course = wait_for(lambda: (c := _course(client, created["id"]))["status"] == "error" and c)
    assert "ANTHROPIC_API_KEY" in course["error"]


def _sample_lesson(client):
    course = client.get("/api/courses").json()[0]
    return client.get(f"/api/courses/{course['id']}").json()["sections"][0]["lessons"][0]["id"]


def test_quiz_marks_answers_and_banks_xp(client, fake_llm):
    lesson_id = _sample_lesson(client)
    started = client.post(f"/api/lessons/{lesson_id}/attempts").json()
    questions = started["questions"]
    assert len(questions) == 10
    assert all("answer_index" not in q and "model_answer" not in q for q in questions)
    assert all(q["id"].startswith(f"{lesson_id}:") for q in questions) and started["fresh"]
    for q in questions:
        body = right_answer(get_store(), started["attempt_id"], q)
        result = client.post(f"/api/attempts/{started['attempt_id']}/answer", json=body).json()
        assert result["verdict"] == "correct"
    again = client.post(f"/api/attempts/{started['attempt_id']}/answer", json={"question_id": questions[0]["id"], "choice": 0})
    assert again.status_code == 409
    done = client.post(f"/api/attempts/{started['attempt_id']}/finish").json()
    assert done["score"] == 1 and done["passed"] and done["first_pass"]
    # 7 mcq x 10 + 3 open x 15 + perfect 15 + pass 20
    assert done["xp"] == 70 + 45 + 15 + 20
    assert done["streak"]["current"] == 1 and done["streak"]["today_done"]
    assert {a["id"] for a in done["achievements"]} >= {"first-steps", "perfect-10"}
    assert done["goal"]["met_now"]
    summary = client.get("/api/summary").json()
    assert summary["xp"]["today"] == 150 and summary["level"]["level"] == 2
    review = client.get(f"/api/attempts/{started['attempt_id']}").json()
    assert review["questions"][0]["result"]["verdict"] == "correct"
    history = client.get("/api/history").json()
    kinds = [e["kind"] for e in history["events"]]
    assert {"quiz_finished", "lesson_passed", "goal_met", "achievement"} <= set(kinds)
    assert history["stats"]["quizzes"] == 1 and history["stats"]["accuracy"] == 1


def test_wrong_answers_fail_the_lesson(client, fake_llm):
    fake_llm.verdict = "incorrect"
    lesson_id = _sample_lesson(client)
    started = client.post(f"/api/lessons/{lesson_id}/attempts").json()
    for q in started["questions"]:
        body = wrong_answer(get_store(), started["attempt_id"], q)
        client.post(f"/api/attempts/{started['attempt_id']}/answer", json=body)
    done = client.post(f"/api/attempts/{started['attempt_id']}/finish").json()
    assert done["score"] == 0 and not done["passed"] and done["xp"] == 0
    assert get_store().lesson(lesson_id)["passed_at"] is None
    # A failed quiz doesn't keep a streak going, but every miss is due for review tomorrow.
    assert done["streak"]["current"] == 0
    assert client.get("/api/review").json()["due"] == 0
    from app import spaced
    from app.db import local_day

    tomorrow = (date.fromisoformat(local_day()) + timedelta(days=1)).isoformat()
    assert len(spaced.due_cards(get_store(), tomorrow, limit=None)) == 10


def test_open_answers_fall_back_to_key_points(client):
    from app import llm, quiz

    llm.set_llm(None)
    question = {"model_answer": "x", "key_points": ["retrieving strengthens memory", "re-reading only builds familiarity"]}
    assert quiz.mark_by_key_points(question, "Retrieval strengthens the memory, while rereading just builds familiarity")[0] == "correct"
    assert quiz.mark_by_key_points(question, "Retrieving it strengthens memory")[0] == "partial"
    assert quiz.mark_by_key_points(question, "I like pizza")[0] == "incorrect"


def test_streaks_and_levels(store):
    today = date.fromisoformat("2026-10-15")
    for offset in (0, 1, 2, 5, 6):
        day = (today - timedelta(days=offset)).isoformat()
        store.insert("events", {"ts": f"{day}T01:00:00+00:00", "day": day, "kind": "quiz_finished", "xp": 10, "detail": {"passed": True}})
    # A failed quiz on day -3 doesn't count.
    store.insert("events", {"ts": "2026-10-12T01:00:00+00:00", "day": "2026-10-12", "kind": "quiz_finished", "xp": 0, "detail": {"passed": False}})
    s = progress.streak(store, today.isoformat())
    assert (s["current"], s["best"], s["today_done"], s["at_risk"], s["freezes"]) == (3, 3, True, False, 0)
    s = progress.streak(store, (today + timedelta(days=1)).isoformat())
    assert s["current"] == 3 and s["at_risk"]
    assert progress.streak(store, (today + timedelta(days=2)).isoformat())["current"] == 0
    assert progress.level_for(0)["level"] == 1
    assert progress.level_for(99)["level"] == 1
    assert progress.level_for(100)["level"] == 2
    assert progress.level_for(300) == {"level": 3, "xp_into": 0, "xp_for_next": 300, "progress": 0.0}


def test_achievement_board_shows_progress(store):
    for offset in range(4):
        day = (date(2026, 10, 1) + timedelta(days=offset)).isoformat()
        store.insert("events", {"ts": f"{day}T01:00:00+00:00", "day": day, "kind": "quiz_finished", "xp": 10, "detail": {"passed": True}})
    board = {a["id"]: a for a in achievements.board(store)}
    assert board["week-warrior"]["value"] == 4 and board["week-warrior"]["target"] == 7
    fresh = {a["id"] for a in achievements.check(store)}
    assert "on-a-roll" in fresh and "week-warrior" not in fresh
    assert achievements.check(store) == []


def test_settings(client):
    assert client.get("/api/settings").json()["daily_goal"] == 50
    assert client.put("/api/settings", json={"daily_goal": 80}).json()["daily_goal"] == 80
    assert client.put("/api/settings", json={"daily_goal": 1}).status_code == 422


def test_delete_course_keeps_history(client):
    course = _create(client)
    assert client.delete(f"/api/courses/{course['id']}").status_code == 204
    assert client.get(f"/api/courses/{course['id']}").status_code == 404
    events = client.get("/api/history").json()["events"]
    assert any(e["kind"] == "course_created" and e["title"] == "heat pumps" for e in events)


def test_svg_sanitizer():
    dirty = ('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" onload="x()">'
             '<foreignObject><div>hi</div></foreignObject><image href="http://evil/x.png"/>'
             '<a href="javascript:alert(1)"><text>t</text></a><use href="#ok"/><rect fill="url(http://e/x)"/>'
             '<rect fill="url(#grad)" style="fill:red"/></svg>')
    clean = svg.sanitize(dirty)
    for bad in ("onload", "foreignObject", "image", "javascript", "http://e", "width="):
        assert bad not in clean
    assert 'href="#ok"' in clean and "url(#grad)" in clean and 'viewBox="0 0 200 100"' in clean
    assert svg.sanitize("not svg") == ""
    assert svg.sanitize('<!DOCTYPE svg [<!ENTITY a "b">]><svg/>') == ""
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg.sanitize('<svg viewBox="0 0 1 1"><rect/></svg>')
