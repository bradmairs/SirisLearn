SHELL := /bin/bash

.PHONY: help up down restart logs status update backend web test

help:
	@echo "SirisLearn"
	@echo "  make up       Build and start (http://<server>:8100)"
	@echo "  make down     Stop"
	@echo "  make restart  Rebuild and restart"
	@echo "  make logs     Follow the logs"
	@echo "  make status   Is it running and healthy?"
	@echo "  make update   git pull, then rebuild and restart"
	@echo "  make backend  API on :8000 for development"
	@echo "  make web      Vite dev server on :5173 (proxies /api to :8000)"
	@echo "  make test     Backend and web tests"

up:
	@test -f .env || (cp .env.example .env && echo "Created .env from .env.example: fill it in, then run make up again." && exit 1)
	docker compose up -d --build

down:
	docker compose down

restart:
	docker compose up -d --build --force-recreate

logs:
	docker compose logs -f --tail=200

status:
	docker compose ps

update:
	git pull
	docker compose up -d --build

backend:
	cd apps/backend && SIRISLEARN_DATA_PATH=../../data uvicorn app.main:app --reload --port 8000

web:
	cd apps/web && npm run dev

test:
	cd apps/backend && python -m pytest -q
	cd apps/web && npx tsc -b --noEmit && npm test
