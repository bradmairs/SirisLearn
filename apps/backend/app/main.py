"""SirisLearn API: health, sign-in, the app's routes, the SirisOS hub routes,
and (in the container) the built web app with its client-side routes."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import api, config, coursepacks, generator, hub, jobs, sample
from app.auth import CurrentUser, check_password, create_token
from app.db import get_store
from app.version import VERSION

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    store = get_store()
    generator.recover(store)
    sample.seed(store)
    coursepacks.seed(store)
    runner = None
    if config.env("SIRISLEARN_JOBS", "true").lower() not in ("0", "false", "no"):
        runner = asyncio.create_task(jobs.run_forever())
    yield
    if runner:
        runner.cancel()


app = FastAPI(title="SirisLearn API", version=VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    username: str


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sirislearn", "version": VERSION}


@app.post("/api/auth/login", response_model=TokenResponse, tags=["auth"])
def login(body: LoginRequest) -> TokenResponse:
    if not check_password(body.username, body.password):
        raise HTTPException(401, "Wrong username or password.")
    token, expires_in = create_token(body.username)
    return TokenResponse(access_token=token, expires_in=expires_in, username=body.username)


@app.get("/api/auth/me", tags=["auth"])
def me(user: CurrentUser) -> dict[str, str]:
    return {"username": user}


app.include_router(api.router)
app.include_router(hub.router)

# The built PWA (apps/web/dist, copied to /app/web in the container).
WEB = Path(__file__).resolve().parent.parent / "web"
if WEB.is_dir():
    app.mount("/assets", StaticFiles(directory=WEB / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str) -> FileResponse:
        if path.startswith("api/"):
            raise HTTPException(404, "Not found.")
        file = (WEB / path).resolve()
        if path and file.is_file() and file.is_relative_to(WEB.resolve()):
            # The service worker must be re-checked on every load to pick up new versions.
            return FileResponse(file, headers={"Cache-Control": "no-cache"} if path == "sw.js" else None)
        return FileResponse(WEB / "index.html", headers={"Cache-Control": "no-cache"})
