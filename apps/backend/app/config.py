"""Settings, read from the environment on every call so tests and redeploys
never see a stale value. Every variable is documented in .env.example."""

from __future__ import annotations

import os
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_MODEL = "claude-opus-5-5"


def env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


def data_dir() -> Path:
    path = Path(env("SIRISLEARN_DATA_PATH", "./data"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def timezone() -> ZoneInfo:
    try:
        return ZoneInfo(env("SIRISLEARN_TIMEZONE", "Australia/Melbourne"))
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def admin_username() -> str:
    return env("SIRISLEARN_ADMIN_USERNAME", "brad")


def admin_password() -> str:
    return env("SIRISLEARN_ADMIN_PASSWORD", "change-me")


def jwt_secret() -> str:
    return env("SIRISLEARN_JWT_SECRET", "change-this-development-secret")


def jwt_expiry_hours() -> int:
    return int(env("SIRISLEARN_JWT_EXPIRY_HOURS", "720"))


def hub_key() -> str:
    """The key SirisOS sends (X-API-Key) to read the hub routes."""
    return env("SIRISLEARN_HUB_KEY")


def llm_provider() -> str:
    """anthropic | ollama | none. Blank picks whichever is configured."""
    chosen = env("SIRISLEARN_LLM_PROVIDER").lower()
    if chosen:
        return chosen
    if env("ANTHROPIC_API_KEY") or env("ANTHROPIC_AUTH_TOKEN"):
        return "anthropic"
    if env("OLLAMA_URL") and env("SIRISLEARN_OLLAMA_MODEL"):
        return "ollama"
    return "none"


def model() -> str:
    return env("SIRISLEARN_MODEL", DEFAULT_MODEL)


def pregenerate() -> str:
    """'next' writes each lesson when it's opened plus the one after it;
    'all' writes the whole course in the background as soon as it's planned."""
    return "all" if env("SIRISLEARN_PREGENERATE", "next").lower() == "all" else "next"


def default_daily_goal() -> int:
    return int(env("SIRISLEARN_DAILY_GOAL", "50"))
