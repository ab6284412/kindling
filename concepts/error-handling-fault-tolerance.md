# Error handling and building fault-tolerant systems
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

A system is fault tolerant when a failure in one part degrades — rather than
kills — the whole. Errors are a design input, not an afterthought: you decide
what happens when a dependency 500s, a write races, or a service restarts.
Sriniously's ▶16 is the dedicated treatment.

## How it works

- **Bounded failure**: assume every external call can fail; add timeouts,
  retries (with backoff + jitter), and circuit breakers so one slow dependency
  doesn't take down the caller.
- **Fail fast with a clear error**: client errors → 4xx with a consistent shape;
  surprises → 5xx. Don't leak stack traces outside.
- **Transactions**: atomic units of work so a partial write is rolled back, not
  half-committed (see [concepts/transactions-acid.md](transactions-acid.md)).
- **Characterize the failure**: is it retryable? timeout vs 4xx vs 500 decide
  whether you retry, back off, or surface to the user.

## How it fails

- **Retrying without backoff**: a thundering herd re-hits a failing service.
- **No timeout**: has been the classic failure mode when the entire world
  hangs.
- **Leaking internals**: `500 {exception: "psycopg2.OperationalError: ..."}`.
- **Catch-all `except Exception`: pass`** hiding real failures — the worst
  "fault tolerance" of all.
- Retrying non-idempotent writes → duplicate charge/like/order. Retry only what
  is safe to repeat (see [concepts/apis-rest-graphql-grpc.md](apis-rest-graphql-grpc.md)).

## Build that proves it

[builds/fastapi-crud.md](../builds/fastapi-crud.md) — wrap handlers with a consistent error
response, add a safe retry with backoff on a flaky call, and a timeout so a
stalled dependency surfaces fast.

## Further reading
- Srinoriously, "Error Handling and Building Fault Tolerant Systems" (▶16) — https://www.youtube.com/watch?v=8NaM_9aKS24 (Jul 8, 2025)