# Build: background worker & a completion webhook
Source: [concepts/message-brokers.md](../concepts/message-brokers.md), and Sriniously's playlist videos ▶14
(Task queues and background jobs) and ▶23 (Concurrency & Parallelism: IO Bound
vs CPU Bound)
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

Goal: move a slow, non-request operation off the request path into an in-process
queue + worker and notify completion via a webhook, proving that request latency
and work time are different things.

## Spec

1. **Baseline (naive)** — `POST /todos` currently does a simulated 3s side
   effect (e.g. `time.sleep(3)` for "send email / generate PDF") inline, so the
   request blocks ~3s. Confirm this first.
2. **Queue** — import `queue.Queue` and `threading.Thread` (stdlib). Start a
   single worker thread in a FastAPI startup `lifespan`.
3. **Deferred** — `POST /todos` enqueues the slow job and returns `202 Accepted`
   immediately with `{"job_id": ...}`. The worker pops jobs and runs them in the
   background.
4. **Job status** — a `jobs(id, todo_id, status, created_at, finished_at)` table
   where `status ∈ queued/running/done/failed`. `GET /jobs/{id}` returns it.
5. **Webhook** — on completion the worker POSTs a payload to the API's own
   `POST /webhooks/local` endpoint (a receiver that records deliveries in a
   `webhooks(id, todo_id, payload, received_at)` table). Failed jobs are marked
   `failed`, with no retry in v1 (retry is an extension).

## Constraints

- Stdlib `queue` + `threading` + FastAPI + psycopg only. No Celery, no Redis,
  no dramatiq.
- In-process queue is fine for v1: note honestly in the build that queued jobs
  are lost on process restart — the production fix is a durable broker
  (extension).
- `time.sleep` in the worker stands in for real IO; say so in the notes.

## Self-check (pass/fail)

```bash
# 1 — 202 comes back fast, well under the 3s it blocks for in the naive version:
time curl -i -X POST localhost:8000/todos -H 'content-type: application/json' \
  -d '{"title":"slow"}'                    # 202, {job_id}, wall time ~ms
# 2 — status transitions within a few seconds:
curl -s localhost:8000/jobs/<job_id>       # queued → done (poll once)
# 3 — webhook delivered:
curl -s localhost:8000/webhooks            # one row for todo_id, payload set
# 4 — the API stays fast while a job runs:
curl -s -w '%{time_total}\n' -o /dev/null localhost:8000/todos   # still quick
```

Also note in the build notes what happens on restart (queued jobs are lost) and
why the CPU-bound case differs: `time.sleep` lets threads overlap, but a tight
`while` loop doing computation is CPU-bound and cannot be sped up by more
threads under the GIL — demonstrate or reference ▶23 for that split.

## Extensions (only after v1 passes)

- Durable queue backed by Postgres (`jobs` as a work table with `FOR UPDATE
  SKIP LOCKED` claim) or Redis.
- Retries with backoff + a dead-letter state.
- Worker pool (N threads); CPU-bound: a `ProcessPoolExecutor` instead (▶23).
- Priority queues / scheduled jobs ([dsa/heaps.md](../dsa/heaps.md) applies).

## Why this matters

Every real product has "send the email", "generate the PDF", "call the partner
API" — the ones that block the request are the ones that time out and wreck
your SLOs. This build makes the request/worker split concrete and shows why
"it blocks for 3s" only matters if you put it on the request path.