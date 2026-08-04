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

## Further reading
- Sriniously, "Logging, Monitoring and Observability" (▶18) — https://www.youtube.com/watch?v=5PEuwgLOQQM (Jul 26, 2025)