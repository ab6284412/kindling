# Concurrency and parallelism: IO-bound vs CPU-bound
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

Concurrency is *structure* (many tasks interleaved, making progress though none
runs simultaneously); parallelism is *hardware* (tasks truly running at once on
multiple cores). Telling which your workload needs — IO-bound vs CPU-bound — is
the whole game. Sriniously's ▶23 closes the playlist on exactly this.

## How it works

- **IO-bound**: the task waits on outside work (DB, network, disk). `asyncio` /
  one thread per request wins; you're waiting, not computing, so interleaving
  is nearly free.
- **CPU-bound**: the task burns local CPU (math, parsing, compression). In
  Python, the GIL blocks threaded parallelism in one process — use
  `multiprocessing`/ProcessPool to use all cores.
- **Lost-update trap**: shared mutable state plus concurrent access needs a lock
  regardless of the model.
- Fan-out: a request hitting several slow services waits on the slowest leg
  (tail latency compounds — see the jargon note).

## How it fails

- Using threads/async for CPU-bound work → 0 speedup (GIL), worse, extra
  scheduling.
- Using multiprocessing for IO-bound work → spawn overhead, no benefit over
  async.
- Shared-state races: incrementing a counter from threads without a lock loses
  updates.
- Fire-and-forget background work without backpressure (see jargon) — the
  queue/threads grow unbounded.

## Drill that proves it

[builds/background-worker.md](../builds/background-worker.md) — move a slow op off the
request path onto a queue + worker, and measure how much an IO wait vs a
CPU-bound chunk each speeds up under Python's GIL.

## Further reading
- Sriniously, "Concurrency & Parallelism: IO Bound vs CPU Bound" (▶23) — https://www.youtube.com/watch?v=bs9MEYRTA30 (Dec 31, 2025)
- [concepts/real-time-data.md](real-time-data.md) — where concurrency meets live streaming.