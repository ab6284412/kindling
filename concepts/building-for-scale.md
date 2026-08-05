# Building for scale
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Martin Fowler

## What it is

The roadmap's sixteenth step: what a service does *under load and under
failure* — **graceful degradation, throttling, backpressure, load shifting,
circuit breakers**, plus the **instrumentation, monitoring, and telemetry**
that tell you it's happening. This is the practical half of
`scaling-databases.md`'s theory.

## The concepts

- **Graceful degradation** — when something fails, degrade features instead
  of dying: serve cached/stale data, disable non-essential parts.
- **Throttling (rate limiting)** — reject or queue requests beyond a limit
  to protect the system from overload and from abusive clients.
- **Backpressure** — instead of buffering indefinitely, push the overload
  *back* to the caller (slow down, return 429/503) so a slow consumer slows
  the producer rather than crashing the system.
- **Load shifting** — move work from overloaded to idle resources: off-peak
  batch jobs, migrating load to another region, using queues to smooth peaks.
- **Circuit breaker** — when a dependency keeps failing, *open the circuit*:
  stop calling it for a while, fail fast with a fallback, then retry.
  See Fowler's post — the canonical reference.
- **Instrumentation / monitoring / telemetry** — metrics, logs, and traces;
  you cannot debug a distributed system you cannot observe.

## How it fails (review checklist)

- **No circuit breaker** — a slow/failing dependency cascades (each request
  waits on it, threads pile up, the whole service degrades).
- **Throttle everything equally** — naive global limits punish good users;
  per-tenant / per-key limits with sensible defaults.
- **Buffering unboundedly** — a queue that never applies backpressure just
  delays the OOM.
- **Monitoring after the incident** — if you can't answer "how much load, how
  many errors, what latency" *right now*, you can't scale anything.

## Build that proves it

No build yet. The drill: wrap one external call in your app with a circuit
breaker (or a hand-rolled "fail after 3 errors, retry in 5s" check), break
the dependency, and show the app degrades instead of hanging.

## Drill

Goal: prove a hand-rolled circuit breaker stops calling a failing dependency
and recovers after a cooldown — stdlib only.

Steps:
1. From a scratch dir, save this as `breaker.py` and run `python3 breaker.py`
   (stdlib only):
   ```python
   import time
   class Breaker:
       def __init__(self, threshold=3, open_seconds=5):
           self.threshold, self.open_seconds = threshold, open_seconds
           self.failures, self.opened_at = 0, None
       def call(self, fn):
           if self.opened_at is not None:
               if time.time() - self.opened_at < self.open_seconds:
                   raise RuntimeError("circuit OPEN — fail fast, no dep call")
               self.failures, self.opened_at = 0, None   # half-open: retry once
           try:
               r = fn()
               self.failures = 0
               return r
           except Exception:
               self.failures += 1
               if self.failures >= self.threshold:
                   self.opened_at = time.time()
               raise
   calls = 0
   def flaky():
       global calls
       calls += 1
       raise ConnectionError("dep down")
   b = Breaker()
   for _ in range(3):
       try: b.call(flaky)
       except ConnectionError: pass
   for _ in range(2):
       try: b.call(flaky)
       except RuntimeError as e: print(e)
   print(f"dependency calls = {calls} (must be 3)")
   ```
2. Read the output.

Self-check (pass/fail — run it alone):
- Prints `dependency calls = 3` — after the 3rd failure the circuit opened;
  calls 4 and 5 raised `RuntimeError` without touching the dependency (the
  two printed "circuit OPEN" lines are the proof).
- Set `open_seconds=1`, add `time.sleep(1.2)` after the third failure, and
  the next `b.call(flaky)` is a half-open retry that fails with
  `ConnectionError` again — the breaker tried again instead of staying shut.

Why this matters: without a breaker every request waits on a dead
dependency and your threads pile up; with one you fail fast and give the
dependency time to recover.

## Further reading
- Sriniously, "Backend Scaling and Performance Part-1/2" (▶21, ▶22) — https://www.youtube.com/watch?v=z7kt_p44rjs, https://www.youtube.com/watch?v=sOhAopEwjH4 (Dec 14, Dec 28 2025)
- roadmap.sh, https://roadmap.sh/backend — "Building For Scale" step
  (fetched Aug 3 2026)
- Martin Fowler, https://martinfowler.com/bliki/CircuitBreaker.html —
  "CircuitBreaker" (fetched Aug 3 2026)
