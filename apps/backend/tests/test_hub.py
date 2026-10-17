"""The routes SirisOS reads."""

from __future__ import annotations

from app.db import get_store


def test_hub_needs_the_key(client):
    assert client.get("/api/hub/v1/status").status_code == 401
    assert client.get("/api/hub/v1/status", headers={"X-API-Key": "wrong"}).status_code == 401


def test_hub_unset_key_is_503(client, monkeypatch):
    monkeypatch.delenv("SIRISLEARN_HUB_KEY")
    assert client.get("/api/hub/v1/status", headers={"X-API-Key": "x"}).status_code == 503


def test_hub_status_summary_search(client):
    key = {"X-API-Key": "hub-key"}
    status = client.get("/api/hub/v1/status", headers=key).json()
    assert status["status"] == "ok" and status["llm"]["configured"]
    summary = client.get("/api/hub/v1/summary", headers=key).json()
    assert summary["streak"]["current"] == 0 and summary["xp"]["goal"] == 50
    assert summary["continue"]["lesson_title"] == "Why we forget, and how to stop it"
    assert summary["continue"]["url"].startswith("/lesson/")
    assert summary["courses"]["active"] == 1
    hits = client.get("/api/hub/v1/search", params={"q": "forget"}, headers=key).json()["hits"]
    assert any(h["kind"] == "lesson" and h["url"].startswith("/lesson/") for h in hits)
    hits = client.get("/api/hub/v1/search", params={"q": "learn anything"}, headers=key).json()["hits"]
    assert hits[0]["kind"] == "course"


def test_hub_reports_streak_at_risk(client):
    store = get_store()
    store.insert("events", {"ts": "2020-01-01T00:00:00+00:00", "day": "2000-01-01", "kind": "quiz_finished", "xp": 10, "detail": {"passed": True}})
    from datetime import date, timedelta

    from app.db import local_day

    yesterday = (date.fromisoformat(local_day()) - timedelta(days=1)).isoformat()
    store.insert("events", {"ts": f"{yesterday}T05:00:00+00:00", "day": yesterday, "kind": "quiz_finished", "xp": 10, "detail": {"passed": True}})
    streak = client.get("/api/hub/v1/summary", headers={"X-API-Key": "hub-key"}).json()["streak"]
    assert streak["current"] == 1 and streak["at_risk"]
