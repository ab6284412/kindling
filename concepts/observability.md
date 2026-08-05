# Logging, monitoring, and observability
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

Observability is making a running system *answer questions*: logs tell you what
happened, metrics tell you how things are trending, and tracing ties a single
request across many services. Without it, production is a black box and every
incident is a guess. Sriniously's ▶18 is the dedicated video.

## How it works

- **Logs**: structured, timestamped events (`level, time, message, request_id,
  user_id`). Grep-able and queryable, not prose.
- **Metrics**: counters and histograms (request rate, latency p50/p99, error
  rate) fed to a dashboard with alerting.
- **Tracing**: a single `request_id` / trace id threaded through every hop so a
  slow request is one story, not N disconnected logs.
- Sanity dashboards: *are requests succeeding? is latency stable? are queues
  draining?*

## How it fails

- **Logs as the only tool**: paging through prose instead of asking 3 questions
  of a metric.
- **No request ids**: can't stitch one user's journey together.
- **Not logging failures**: only happy-path logs, so incidents leave no trail.
- **Logging secrets**: tokens, password hashes, PII in plaintext logs.
- **Too much / too little**: massive debug noise or nothing at all — tune the
  level, keep a redacted summary always.

## Build that proves it

[builds/production-deploy.md](../builds/production-deploy.md) — add structured logging with a
request id, emit a latency metric, and a `/ready` that reflects real health.

## Drill

Goal: prove structured JSON-lines logs with a `request_id` let you stitch
one request together — stdlib `logging` only.

Steps:
1. From a scratch dir, save this as `app.py` and run `python3 app.py`
   (stdlib only):
   ```python
   import json, logging, time, uuid
   class JsonFormatter(logging.Formatter):
       def format(self, r):
           return json.dumps({"t": time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime(r.created)),
                              "level": r.levelname,
                              "request_id": getattr(r, "request_id", "-"),
                              "path": getattr(r, "path", "-"),
                              "status": getattr(r, "status", "-")})
   logging.basicConfig(level=logging.INFO, format="%(message)s",
                       handlers=[logging.FileHandler("app.log")])
   log = logging.getLogger("app")
   for h in logging.getLogger().handlers:     # root owns the FileHandler
       h.setFormatter(JsonFormatter())
   def handle(path, status):
       rid = uuid.uuid4().hex[:8]
       log.info("request", extra={"request_id": rid, "path": path, "status": status})
   handle("/users", 200)
   handle("/users/42", 500)
   handle("/users", 200)
   ```
2. Inspect the log: `cat app.log` — one JSON object per line, three lines.
3. Pick a `request_id` from one line and `grep <that-id> app.log`.

Self-check (pass/fail — run it alone):
- Every line parses as JSON (pipe one through `python3 -m json.tool`) and has
  `request_id`, `path`, and `status`.
- The 500 line is present with the same shape as the 200s — failures leave a
  trail, not silence.
- `grep <request_id> app.log` returns exactly the line(s) for that one
  request, and the 500's id greps to its own single line.

Why this matters: in production the question is "what happened to *this*
request" — prose logs can't answer it; one id per line can.

## Further reading
- Sriniously, "Logging, Monitoring and Observability" (▶18) — https://www.youtube.com/watch?v=5PEuwgLOQQM (Jul 26, 2025)