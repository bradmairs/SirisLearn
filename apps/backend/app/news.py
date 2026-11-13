"""Recent AI news, read from public RSS and Atom feeds, for the monthly
"What's new in AI" lesson and for refreshing AI lessons.

The feeds are SIRISLEARN_AI_FEEDS (comma-separated URLs), defaulting to a
few AI news and lab blogs. Items from the last 35 days are kept: title,
source, date, link and a short plain-text summary. Feed text is untrusted:
it's parsed with defusedxml, stripped of HTML and handed to the model as
data to summarise, never as instructions. A feed that fails is skipped.
"""

from __future__ import annotations

import asyncio
import html
import logging
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import httpx
from defusedxml import ElementTree

from app import config

logger = logging.getLogger(__name__)

DEFAULT_FEEDS = [
    "https://openai.com/news/rss.xml",
    "https://blog.google/technology/ai/rss/",
    "https://huggingface.co/blog/feed.xml",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://aws.amazon.com/blogs/machine-learning/feed/",
]
HEADERS = {"User-Agent": "SirisLearn/1.4 (private learning app; https://github.com/bradmairs/SirisLearn)"}
MAX_ITEMS = 40
ATOM = "{http://www.w3.org/2005/Atom}"

# Tests swap this for an httpx.MockTransport.
transport: httpx.AsyncBaseTransport | None = None


def feeds() -> list[str]:
    raw = config.env("SIRISLEARN_AI_FEEDS", "")
    return [u.strip() for u in raw.split(",") if u.strip().startswith("https://")] if raw.strip() else list(DEFAULT_FEEDS)


def _text(value: str | None, limit: int = 400) -> str:
    plain = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    plain = re.sub(r"\s+", " ", plain).strip()
    return plain[:limit].rsplit(" ", 1)[0] + "…" if len(plain) > limit else plain


def _date(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    try:
        moment = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def parse(xml: str, source: str) -> list[dict[str, Any]]:
    """RSS 2.0 <item>s or Atom <entry>s as plain dicts."""
    try:
        root = ElementTree.fromstring(xml)
    except Exception:
        logger.warning("Couldn't read the feed from %s", source)
        return []
    title = _text(root.findtext("channel/title") or root.findtext(f"{ATOM}title") or source, 80)
    items = []
    for node in root.iter("item"):
        items.append({"title": _text(node.findtext("title"), 200), "link": (node.findtext("link") or "").strip(),
                      "published": _date(node.findtext("pubDate") or node.findtext("{http://purl.org/dc/elements/1.1/}date")),
                      "summary": _text(node.findtext("description")), "source": title})
    for node in root.iter(f"{ATOM}entry"):
        link = next((l.get("href") for l in node.findall(f"{ATOM}link") if l.get("rel") in (None, "alternate")), "")
        items.append({"title": _text(node.findtext(f"{ATOM}title"), 200), "link": (link or "").strip(),
                      "published": _date(node.findtext(f"{ATOM}published") or node.findtext(f"{ATOM}updated")),
                      "summary": _text(node.findtext(f"{ATOM}summary") or node.findtext(f"{ATOM}content")), "source": title})
    return [i for i in items if i["title"] and i["link"].startswith("https://")]


async def _fetch(client: httpx.AsyncClient, url: str) -> list[dict[str, Any]]:
    try:
        response = await client.get(url)
        response.raise_for_status()
        return parse(response.text[:2_000_000], url)
    except (httpx.HTTPError, ValueError):
        logger.warning("Couldn't fetch the feed %s", url, exc_info=True)
        return []


async def recent(days: int = 35, now: datetime | None = None) -> list[dict[str, Any]]:
    """The newest items across every feed, newest first, deduplicated by link."""
    now = now or datetime.now(timezone.utc)
    since = now - timedelta(days=days)
    async with httpx.AsyncClient(timeout=20, headers=HEADERS, follow_redirects=True, transport=transport) as client:
        batches = await asyncio.gather(*(_fetch(client, url) for url in feeds()))
    seen: set[str] = set()
    out = []
    for item in sorted((i for b in batches for i in b if i["published"] and i["published"] >= since),
                       key=lambda i: i["published"], reverse=True):
        if item["link"] in seen:
            continue
        seen.add(item["link"])
        out.append({**item, "published": item["published"].date().isoformat()})
    return out[:MAX_ITEMS]


def as_prompt(items: list[dict[str, Any]]) -> str:
    lines = [f"- [{i['published']}] {i['source']}: {i['title']}\n  {i['summary']}\n  {i['link']}" for i in items]
    return "<news_items>\n" + "\n".join(lines) + "\n</news_items>"
