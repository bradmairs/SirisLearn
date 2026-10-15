FROM node:22-alpine AS web-build
WORKDIR /src/apps/web
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY apps/web/ ./
RUN npm run build

FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SIRISLEARN_DATA_PATH=/app/data
WORKDIR /app
COPY apps/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY apps/backend/app /app/app
COPY --from=web-build /src/apps/web/dist /app/web
RUN mkdir -p /app/data
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=15s --retries=8 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()" || exit 1
# One worker: lessons are written by background tasks inside the API process.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
