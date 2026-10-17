"""The model that writes courses and marks open answers.

Two providers, chosen by SIRISLEARN_LLM_PROVIDER (or whichever is set up):

- `anthropic` (default when ANTHROPIC_API_KEY is set): Claude through the
  official SDK, with structured JSON outputs, prompt caching on the stable
  instructions and course plan, and server-side refusal fallback.
- `ollama`: a model on your LAN Ollama (OLLAMA_URL + SIRISLEARN_OLLAMA_MODEL),
  using Ollama's JSON-schema `format`. Cheaper, and the quality depends on
  the model.

Every call returns a parsed JSON object that matches the schema it was given.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Protocol

import anthropic
import httpx

from app import config

logger = logging.getLogger(__name__)

# $ per million tokens: input, output, cache read, cache write (5-minute).
PRICES: dict[str, tuple[float, float, float, float]] = {
    "claude-opus-5-5": (4.0, 20.0, 0.20, 5.0),
    "claude-opus-5": (5.0, 25.0, 0.50, 6.25),
    "claude-opus-4-8": (5.0, 25.0, 0.50, 6.25),
    "claude-sonnet-5-5": (2.0, 10.0, 0.20, 2.5),
    "claude-haiku-5-5": (0.10, 0.50, 0.01, 0.125),
    "claude-fable-5-1": (10.0, 50.0, 0.25, 12.5),
}


def cost(model: str, input_tokens: int, output_tokens: int, cache_read: int = 0, cache_write: int = 0) -> float:
    price = PRICES.get(model) or next((p for name, p in PRICES.items() if model.startswith(name)), None)
    if price is None:
        return 0.0
    return (input_tokens * price[0] + output_tokens * price[1] + cache_read * price[2] + cache_write * price[3]) / 1_000_000


def record_usage(model: str, meta: dict[str, Any] | None, input_tokens: int, output_tokens: int,
                 cache_read: int = 0, cache_write: int = 0) -> None:
    """Log one model call's tokens and estimated cost (Settings shows the totals)."""
    from app.db import get_store, now_iso

    meta = meta or {}
    try:
        get_store().insert("usage", {
            "ts": now_iso(), "purpose": meta.get("purpose") or "other", "model": model,
            "course_id": meta.get("course_id"), "lesson_id": meta.get("lesson_id"),
            "input_tokens": input_tokens, "output_tokens": output_tokens,
            "cache_read_tokens": cache_read, "cache_write_tokens": cache_write,
            "cost": round(cost(model, input_tokens, output_tokens, cache_read, cache_write), 6),
        })
    except Exception:  # never fail a lesson over bookkeeping
        logger.warning("Couldn't record model usage", exc_info=True)


class LLMError(Exception):
    """A generation failure worth showing to the user."""


class LLM(Protocol):
    name: str

    async def json(self, *, system: str, context: str, prompt: str, schema: dict[str, Any],
                   effort: str = "medium", max_tokens: int = 32000, meta: dict[str, Any] | None = None) -> dict[str, Any]:
        """`system` is the frozen instructions, `context` the per-course part
        that repeats across that course's calls, `prompt` the request.
        `meta` (purpose, course_id, lesson_id) labels the call in the usage log."""
        ...


class ClaudeLLM:
    name = "anthropic"

    def __init__(self, model: str) -> None:
        self.model = model
        self.client = anthropic.AsyncAnthropic(max_retries=3)

    async def json(self, *, system: str, context: str, prompt: str, schema: dict[str, Any],
                   effort: str = "medium", max_tokens: int = 32000, meta: dict[str, Any] | None = None) -> dict[str, Any]:
        # Stable prefix first (instructions, then this course's plan), each
        # cached, so every lesson of a course reuses the same cached prefix.
        system_blocks: list[dict[str, Any]] = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        if context:
            system_blocks.append({"type": "text", "text": context, "cache_control": {"type": "ephemeral"}})
        try:
            async with self.client.beta.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                system=system_blocks,
                messages=[{"role": "user", "content": prompt}],
                output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                message = await stream.get_final_message()
        except anthropic.AuthenticationError as exc:
            raise LLMError("Claude rejected the API key (ANTHROPIC_API_KEY).") from exc
        except anthropic.RateLimitError as exc:
            raise LLMError("Claude is rate limiting requests. Try again in a minute.") from exc
        except anthropic.BadRequestError as exc:
            raise LLMError(f"Claude couldn't take the request: {exc.message}") from exc
        except anthropic.APIStatusError as exc:
            raise LLMError(f"Claude returned an error ({exc.status_code}). Try again shortly.") from exc
        except anthropic.APIConnectionError as exc:
            raise LLMError("Couldn't reach Claude. Check the server's internet connection.") from exc

        if message.stop_reason == "refusal":
            raise LLMError("Claude declined to write this. Try rewording the topic.")
        if message.stop_reason == "max_tokens":
            raise LLMError("The answer was cut off before it finished. Try again.")
        usage = message.usage
        logger.info("claude %s: in=%s cache_read=%s cache_write=%s out=%s", message.model, usage.input_tokens,
                    usage.cache_read_input_tokens, usage.cache_creation_input_tokens, usage.output_tokens)
        record_usage(str(message.model or self.model), meta, usage.input_tokens or 0, usage.output_tokens or 0,
                     usage.cache_read_input_tokens or 0, usage.cache_creation_input_tokens or 0)
        text = next((b.text for b in message.content if b.type == "text"), "")
        return _parse(text)


class OllamaLLM:
    name = "ollama"

    def __init__(self, url: str, model: str) -> None:
        self.url = url.rstrip("/")
        self.model = model

    async def json(self, *, system: str, context: str, prompt: str, schema: dict[str, Any],
                   effort: str = "medium", max_tokens: int = 32000, meta: dict[str, Any] | None = None) -> dict[str, Any]:
        body = {
            "model": self.model,
            "stream": False,
            "format": schema,
            "options": {"temperature": 0.4, "num_predict": max_tokens},
            "messages": [
                {"role": "system", "content": f"{system}\n\n{context}".strip()},
                {"role": "user", "content": prompt},
            ],
        }
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(900.0, connect=10.0)) as client:
                response = await client.post(f"{self.url}/api/chat", json=body)
        except httpx.HTTPError as exc:
            raise LLMError(f"Couldn't reach Ollama at {self.url}.") from exc
        if response.status_code >= 400:
            raise LLMError(f"Ollama returned {response.status_code}: {response.text[:200]}")
        data = response.json() or {}
        record_usage(f"ollama:{self.model}", meta, int(data.get("prompt_eval_count") or 0), int(data.get("eval_count") or 0))
        return _parse((data.get("message") or {}).get("content") or "")


def _parse(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except ValueError as exc:
        raise LLMError("The model's answer wasn't valid JSON. Try again.") from exc
    if not isinstance(value, dict):
        raise LLMError("The model's answer wasn't a JSON object. Try again.")
    return value


_override: LLM | None = None


def get_llm() -> LLM | None:
    """The configured model, or None when no provider is set up."""
    if _override is not None:
        return _override
    provider = config.llm_provider()
    if provider == "anthropic":
        return ClaudeLLM(config.model())
    if provider == "ollama" and config.env("OLLAMA_URL") and config.env("SIRISLEARN_OLLAMA_MODEL"):
        return OllamaLLM(config.env("OLLAMA_URL"), config.env("SIRISLEARN_OLLAMA_MODEL"))
    return None


def set_llm(llm: LLM | None) -> None:
    """Tests: swap in a fake model."""
    global _override
    _override = llm


def describe() -> dict[str, Any]:
    llm = get_llm()
    if llm is None:
        return {"provider": "none", "model": None, "configured": False}
    return {"provider": llm.name, "model": getattr(llm, "model", None), "configured": True}
