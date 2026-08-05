# Real-time data
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Mozilla Contributors

## What it is

The roadmap's real-time step: pushing updates to clients *as they happen*
instead of the client polling — **long/short polling, WebSockets, and
Server-Sent Events**. The roadmap's real-time cluster also pulls in the
realtime-flavored datastores (Redis pub/sub, DynamoDB Streams, Firebase).

## The concepts

- **Short polling** — the client asks repeatedly ("anything new?"); simple,
  wasteful, latency = poll interval.
- **Long polling** — the server holds the request until something changes
  (or a timeout), then responds; the "poor man's push."
- **WebSockets** — a persistent full-duplex TCP connection; both sides push
  anytime. The tool for chat, games, live collaboration.
- **Server-Sent Events (SSE)** — a one-way server→client stream over plain
  HTTP (text/event-stream); simpler than WebSockets (auto-reconnect built
  in) when you only need server pushes.

## How it works

Choosing between them is choosing the direction and persistence of the
stream: SSE for one-way server→client over HTTP; WebSockets for true
bidirectional; long/short polling when you can't hold connections (some
proxies/load balancers). All of them are about *latency*: how fast can the
client learn what changed.

## How it fails (review checklist)

- **WebSockets when SSE suffices** — full-duplex adds a different protocol,
  connection handling, and proxy/firewall pain you don't need for a
  notification feed.
- **No heartbeat/reconnect** — silent dead connections; both WebSocket ping
  frames and SSE auto-reconnect exist for a reason.
- **Scaling the socket layer** — every connected client is a long-lived
  connection; sticky sessions/Redis pub-sub appear the moment you run more
  than one server instance.
- **Polling too fast** — DDOS-ing your own API with 1-second polls when a
  ​​proper channel exists.

## Build that proves it

No build yet. The drill: serve a live-updating counter to a page three
ways — short polling, SSE, and WebSockets — and measure the latency and
connection count of each.

## Drill

Goal: prove server-push (SSE) delivers events without the client polling,
using only stdlib `http.server` and `urllib`.

Steps:
1. From a scratch dir, save this as `sse.py` and run `python3 sse.py`
   (stdlib only):
   ```python
   import time
   from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
   class H(BaseHTTPRequestHandler):
       def do_GET(self):
           if self.path != "/events":
               self.send_error(404); return
           self.send_response(200)
           self.send_header("Content-Type", "text/event-stream")
           self.end_headers()
           for i in range(3):
               self.wfile.write(f"data: tick {i}\n\n".encode())
               self.wfile.flush()
               time.sleep(1)
       def log_message(self, *a): pass
   ThreadingHTTPServer(("127.0.0.1", 8123), H).serve_forever()
   ```
2. In a second terminal, read the stream — the client has *no* loop and no
   timer, it just blocks on the socket:
   ```python
   import urllib.request
   for line in urllib.request.urlopen("http://127.0.0.1:8123/events"):
       print(line.decode().strip())
   ```
3. Watch the client print `data: tick 0`, `1`, `2` one per second with zero
   client-side polling code — the server pushed, the client waited.

Self-check (pass/fail — run it alone):
- The client prints three `data: tick N` lines, one per second, with a single
  `urlopen` call and no `while` loop.
- Kill the server mid-stream: the client raises `ConnectionResetError` — it
  learns the stream ended only because the *connection* died, not because a
  poll returned empty.

Why this matters: SSE is the cheap way to push updates over plain HTTP; if
you can hold a connection you never need to poll your own API.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Real-Time Data" step
  (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API —
  "The WebSocket API" (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events —
  "Server-sent events" (fetched Aug 3 2026)
