"""Single-user sign-in (the same model as SirisOS) and the hub key SirisOS
uses to read the widget, search and status routes."""

from __future__ import annotations

import hmac
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException

from app import config

JWT_ALGORITHM = "HS256"
ISSUER = "sirislearn-api"


def create_token(username: str) -> tuple[str, int]:
    expires_in = config.jwt_expiry_hours() * 3600
    now = datetime.now(timezone.utc)
    payload = {"sub": username, "iat": now, "exp": now + timedelta(seconds=expires_in), "iss": ISSUER}
    return jwt.encode(payload, config.jwt_secret(), algorithm=JWT_ALGORITHM), expires_in


def check_password(username: str, password: str) -> bool:
    return hmac.compare_digest(username, config.admin_username()) and hmac.compare_digest(password, config.admin_password())


def require_user(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Authentication required.", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(
            authorization.removeprefix("Bearer ").strip(), config.jwt_secret(), algorithms=[JWT_ALGORITHM], issuer=ISSUER
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(401, "Invalid or expired session.", headers={"WWW-Authenticate": "Bearer"}) from exc
    if payload.get("sub") != config.admin_username():
        raise HTTPException(401, "Invalid session user.")
    return payload["sub"]


def require_hub_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    expected = config.hub_key()
    if not expected:
        raise HTTPException(503, "The SirisOS hub key isn't set (SIRISLEARN_HUB_KEY).")
    if not x_api_key or not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(401, "Missing or invalid X-API-Key.")


CurrentUser = Annotated[str, Depends(require_user)]
