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

## Drill

Goal: prove with a stopwatch that threads overlap IO waits but not CPU work.

Steps:
1. From a scratch dir, save this as `work.py` — the two worker stubs are yours
   to fill in; the timing harness below them is complete:
   ```python
   import time
   from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

   def run_io(i):
       # FILL IN: an IO wait, e.g. time.sleep(1)
       raise NotImplementedError("fill in run_io")

   def run_cpu(i):
       # FILL IN: ~1s of CPU, e.g. sum up to a big number
       raise NotImplementedError("fill in run_cpu")

   def bench(fn, label):
       t0 = time.perf_counter()
       list(map(fn, range(4)))                       # 1 thread: baseline
       print(f"{label} 1 thread   : {time.perf_counter() - t0:.2f}s")
       t0 = time.perf_counter()
       with ThreadPoolExecutor(max_workers=4) as ex:
           list(ex.map(fn, range(4)))                # 4 threads
       print(f"{label} 4 threads  : {time.perf_counter() - t0:.2f}s")
       if fn is run_cpu:
           t0 = time.perf_counter()
           with ProcessPoolExecutor(max_workers=4) as ex:
               list(ex.map(fn, range(4)))            # 4 processes
           print(f"{label} 4 processes: {time.perf_counter() - t0:.2f}s")

   if __name__ == "__main__":   # guard: on macOS spawn re-runs this file in children
       bench(run_io, "io ")
       bench(run_cpu, "cpu")
   ```
2. Fill in the two stubs — `run_io` with `time.sleep(1)`, `run_cpu` with a
   tight loop that burns ~1s of CPU (e.g. sum to a big number) — so each call
   returns after roughly the same ~1s of work.
3. Run `python3 work.py` and read the wall times.

Self-check: the IO case drops from ~4s to ~1s with threads (they overlap the
wait); the CPU case stays ~4s with threads (GIL serializes it) but drops to ~1s
with processes (real cores). If your numbers don't show that split, you've hit
the exact mental model this drill exists to fix.

Why this matters: "make it faster with threads" is the junior default, and it
only works for IO — picking the model by workload class (▶23) is the
senior-level reflex.

## Further reading
- Sriniously, "Concurrency & Parallelism: IO Bound vs CPU Bound" (▶23) — https://www.youtube.com/watch?v=bs9MEYRTA30 (Dec 31, 2025)
- [concepts/real-time-data.md](real-time-data.md) — where concurrency meets live streaming.