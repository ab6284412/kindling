"""Reference solution for builds/production-deploy.md — run it like a service.

12-factor config (env with defaults), JSON-lines logs with request ids, /health
vs /ready, minimal /metrics, graceful-shutdown lifespan, non-secret logging.

SIGTERM handling is left to uvicorn: its default handler runs the lifespan
shutdown and waits for in-flight requests, so `docker stop` exits cleanly.
Run: uvicorn app:app   (or the Dockerfile in this dir)
"""
import json
import logging
import os
import time
import uuid

import psycopg
from fastapi import FastAPI, Request, Response
from starlette.responses import PlainTextResponse

DATABASE_URL = os.environ.get("DATABASE_URL", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# --- structured JSON-lines logging ------------------------------------------
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for key in ("request_id", "method", "path", "status", "duration_ms"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        return json.dumps(payload)


_handler = logging.StreamHandler()
_handler.setFormatter(JsonFormatter())
root = logging.getLogger()
root.handlers = [_handler]
root.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
log = logging.getLogger("api")

# --- app + metrics ------------------------------------------------------------
app = FastAPI()
_requests = 0
_latency: dict[str, int] = {}  # bucket ("<10ms", "<100ms", ...) -> count
_started = time.time()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    global _requests
    rid = str(uuid.uuid4())
    t0 = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - t0) * 1000
    _requests += 1
    for b, lo, hi in (("<10ms", 0, 10), ("<100ms", 10, 100), ("<1s", 100, 1000), (">=1s", 1000, float("inf"))):
        if lo <= ms < hi:
            _latency[b] = _latency.get(b, 0) + 1
            break
    if not response.headers.get("x-request-id"):
        response.headers["x-request-id"] = rid
    log.info(
        "request",
        extra={
            "request_id": rid,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(ms, 1),
        },
    )
    return response


@app.on_event("startup")
def startup() -> None:
    log.info("startup complete")


@app.on_event("shutdown")
def shutdown() -> None:
    log.info("shutdown: uvicorn drained in-flight requests before this ran")


@app.get("/health")
def health():
    return {"status": "ok"}  # liveness: is the process alive?


@app.get("/ready")
def ready():
    if not DATABASE_URL:
        return Response("no DATABASE_URL configured", status_code=503)
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=2):
            return {"status": "ready"}  # readiness: can it serve? DB reachable?
    except Exception:  # noqa: BLE001 - any DB failure means not ready
        return Response("db unreachable", status_code=503)


@app.get("/metrics")
def metrics():
    lines = [
        f"process_uptime_seconds {time.time() - _started:.0f}",
        f"http_requests_total {_requests}",
    ] + [f'http_request_duration_bucket{{le="{b}"}} {c}' for b, c in sorted(_latency.items())]
    return PlainTextResponse("\n".join(lines) + "\n")
