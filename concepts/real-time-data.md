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

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Real-Time Data" step
  (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API —
  "The WebSocket API" (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events —
  "Server-sent events" (fetched Aug 3 2026)
