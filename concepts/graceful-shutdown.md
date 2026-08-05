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

## Drill

Goal: prove a SIGTERM handler drains an in-flight request to completion
instead of cutting it — stdlib `http.server` only.

Steps:
1. From a scratch dir, save this as `server.py` and run `python3 server.py`:
   ```python
   import signal, threading, time
   from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
   class H(BaseHTTPRequestHandler):
       def do_GET(self):
           if self.path == "/slow":
               time.sleep(3)
           self.send_response(200); self.end_headers()
           self.wfile.write(b"done")
       def log_message(self, *a): pass
   server = ThreadingHTTPServer(("127.0.0.1", 8122), H)
   server.daemon_threads = False   # non-daemon handlers: server_close() joins them
   def stop(sig, frame):
       print("SIGTERM: stopping accept, draining in-flight", flush=True)
       threading.Thread(target=server.shutdown).start()
   signal.signal(signal.SIGTERM, stop)
   server.serve_forever()
   server.server_close()      # drain: join in-flight handler threads
   print("exited cleanly", flush=True)
   ```
2. In a second terminal, start a slow request, then terminate the server
   while it's running:
   - `curl http://127.0.0.1:8122/slow &`
   - `kill -TERM $(pgrep -f server.py)`
3. Watch both terminals.

Self-check (pass/fail — run it alone):
- The in-flight curl still prints `done` (HTTP 200) even though SIGTERM
  arrived mid-request — the handler stopped accepting *new* work but let the
  in-flight one finish.
- The server terminal prints "SIGTERM: stopping accept" then "exited
  cleanly" only *after* the curl finished.
- Repeat step 2 but with `kill -9`: the curl dies mid-request with a
  connection reset — the contrast is the point.

Why this matters: orchestrators (k8s, Docker stop) send SIGTERM then
escalate; if you don't drain, every deploy cuts a write or a job mid-flight.

## Further reading
- Sriniously, "Graceful Shutdown" (▶19) — https://www.youtube.com/watch?v=6rfBgphiCWM (Sep 19, 2025)