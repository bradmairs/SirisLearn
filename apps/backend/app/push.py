"""Phone notifications (Web Push), for the installed PWA.

SirisLearn makes its own VAPID key pair on first use (data/vapid.pem), the
browser subscribes with the public key, and the scheduler (app/jobs.py)
sends the reminders. On iPhone, notifications work for the app added to the
home screen (iOS 16.4+), not in a Safari tab.
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
from typing import Any

from app import config
from app.db import Store, now_iso

logger = logging.getLogger(__name__)


def _key_path():
    return config.data_dir() / "vapid.pem"


def _vapid():
    from py_vapid import Vapid02

    path = _key_path()
    if path.exists():
        return Vapid02.from_file(str(path))
    vapid = Vapid02()
    vapid.generate_keys()
    vapid.save_key(str(path))
    return vapid


def public_key() -> str:
    """The application server key the browser subscribes with (base64url)."""
    from cryptography.hazmat.primitives import serialization

    raw = _vapid().public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def status(store: Store) -> dict[str, Any]:
    n = store.one("SELECT COUNT(*) AS n FROM push_subscriptions") or {"n": 0}
    return {"subscriptions": n["n"], "reminder_hour": reminder_hour(), "review_hour": review_hour()}


def reminder_hour() -> int:
    return int(config.env("SIRISLEARN_REMINDER_HOUR", "19"))


def review_hour() -> int:
    return int(config.env("SIRISLEARN_REVIEW_HOUR", "8"))


def subscribe(store: Store, subscription: dict[str, Any]) -> None:
    endpoint = str(subscription.get("endpoint") or "")
    keys = subscription.get("keys") or {}
    if not endpoint.startswith("https://") or not keys.get("p256dh") or not keys.get("auth"):
        raise ValueError("That isn't a valid push subscription.")
    store.run("INSERT INTO push_subscriptions (endpoint, subscription, created_at) VALUES (?, ?, ?)"
              " ON CONFLICT(endpoint) DO UPDATE SET subscription = excluded.subscription", endpoint, json.dumps(subscription), now_iso())


def unsubscribe(store: Store, endpoint: str) -> None:
    store.run("DELETE FROM push_subscriptions WHERE endpoint = ?", endpoint)


def _send_one(subscription: dict[str, Any], payload: dict[str, Any]) -> int:
    from pywebpush import WebPushException, webpush

    contact = config.env("SIRISLEARN_PUSH_CONTACT", "mailto:admin@localhost")
    try:
        webpush(subscription_info=subscription, data=json.dumps(payload), vapid_private_key=_vapid(),
                vapid_claims={"sub": contact}, ttl=12 * 3600, timeout=10)
        return 201
    except WebPushException as exc:
        return exc.response.status_code if exc.response is not None else 0


# Tests replace this to capture what would be sent.
sender = _send_one


async def send(store: Store, title: str, body: str, url: str = "/", tag: str = "sirislearn") -> int:
    """Send to every subscribed device; returns how many accepted it.
    Subscriptions the push service says are gone (404/410) are removed."""
    sent = 0
    payload = {"title": title, "body": body, "url": url, "tag": tag}
    for row in store.all("SELECT * FROM push_subscriptions"):
        code = await asyncio.to_thread(sender, row["subscription"], payload)
        if code in (404, 410):
            unsubscribe(store, row["endpoint"])
        elif 200 <= code < 300:
            sent += 1
        else:
            logger.info("Push to %s… failed with %s", row["endpoint"][:40], code)
    return sent
