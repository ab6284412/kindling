# Graceful shutdown
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

Graceful shutdown is what a process does *between* "kill signal received" and
"exited": stop accepting new work, finish in-flight requests and jobs, flush
state, then exit with a clean status — instead of dying mid-write. Sriniously's
▶19 covers it.

## How it works

- When SIGTERM/SIGINT arrives, the process: (1) unregisters from the load
  balancer / stops accepting new connections, (2) drains in-flight requests to
  completion within a deadline, (3) flushes buffers / closes DB pools, (4) exits
  non-zero only if there was a problem.
- A stop-deadline bounds draining so the process can't hang forever; after
  the timeout, force-exit.
- Background workers drain their current job, then stop pulling new ones.

## How it fails

- **Kill -9 as routine**: no signal handling → in-flight writes/DB transactions
  cut mid-commit.
- **Ignoring in-flight work**: shutdown handler returns instantly, dropping
  active requests.
- **No deadline**: the process waits forever on a stuck request and never exits
  for the orchestrator.
- Double-pipelining: handler starts *new* work during shutdown instead of only
  draining.
- Not flushing: buffered logs/metrics lost on exit.

## Build that proves it

[builds/production-deploy.md](../builds/production-deploy.md) — register signal handlers that
stop the accept loop, drain in-flight requests with a deadline, and flush before
exiting; verify a request in flight completes during shutdown.

## Further reading
- Sriniously, "Graceful Shutdown" (▶19) — https://www.youtube.com/watch?v=6rfBgphiCWM (Sep 19, 2025)