"""Real photographs for lessons, from Wikimedia Commons.

The model gives each lesson a short search (`photo_query`), and this finds a
freely licensed photo for it and keeps its credit: title, author, licence and
the Commons page. The browser shows the photo from upload.wikimedia.org with
that credit underneath. No key is needed. Set SIRISLEARN_PHOTOS=false to turn
it off.
"""

from __future__ import annotations

import html
import logging
import re
from typing import Any

import httpx

from app import config

logger = logging.getLogger(__name__)

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "SirisLearn/1.0 (private learning app; https://github.com/bradmairs/SirisLearn)"}
OPEN_LICENCES = ("cc0", "cc by", "cc-by", "public domain", "pd", "attribution")

# Tests swap this for an httpx.MockTransport.
transport: httpx.AsyncBaseTransport | None = None


def enabled() -> bool:
    return config.env("SIRISLEARN_PHOTOS", "true").lower() not in ("0", "false", "no")


def _text(value: Any) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", str(value or ""))).strip()


async def find(query: str) -> dict[str, Any] | None:
    """The best freely licensed photo for a search, or None."""
    query = (query or "").strip()
    if not query or not enabled():
        return None
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6, "gsrlimit": 8, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1200,
    }
    try:
        async with httpx.AsyncClient(timeout=10.0, headers=HEADERS, transport=transport) as client:
            response = await client.get(API, params=params)
            response.raise_for_status()
            pages = (response.json().get("query") or {}).get("pages") or {}
    except (httpx.HTTPError, ValueError):
        logger.info("Wikimedia search for %r failed", query, exc_info=True)
        return None
    for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        licence = _text((meta.get("LicenseShortName") or {}).get("value"))
        if not info.get("thumburl") or not any(word in licence.lower() for word in OPEN_LICENCES):
            continue
        if (info.get("width") or 0) < 400:
            continue
        return {
            "url": info["thumburl"],
            "page": info.get("descriptionurl") or "",
            "title": _text((meta.get("ObjectName") or {}).get("value")) or str(page.get("title", "")).removeprefix("File:").rsplit(".", 1)[0],
            "author": _text((meta.get("Artist") or {}).get("value"))[:120] or "Unknown author",
            "licence": licence,
            "query": query,
        }
    return None
