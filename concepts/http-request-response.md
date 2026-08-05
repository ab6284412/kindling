# HTTP: the request/response model
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: R. Fielding, M. Nottingham, J. Reschke (RFC 9110); MDN contributors

## What it is

HTTP is a client-server protocol built on one idea: every interaction is an
independent **request** followed by a **response**. A request has a request
line, headers, and an optional body; a response has a status line, headers,
and an optional body.

```
GET /items/42 HTTP/1.1          <- request line: METHOD SP target SP version
Host: api.example.com           <- headers (case-insensitive names)
Accept: application/json
                                 <- blank line ends headers
                                 <- body (absent here)

HTTP/1.1 200 OK                 <- status line: version SP code SP reason
Content-Type: application/json
Content-Length: 27
                                 <- blank line
{"id":42,"name":"widget"}
```

The model is **stateless**: the server stores nothing about a request between
requests. Anything that must survive between requests travels in a header
(`Cookie`, `Authorization`) or in the resource itself.

## Key semantics

- **Methods**: `GET` (safe: no side effects; idempotent; conventionally no
  body), `HEAD` (GET without body), `POST` (neither safe nor idempotent —
  creates a resource), `PUT` (idempotent — replace), `PATCH` (partial update,
  not idempotent), `DELETE` (idempotent). Idempotent means "same request, same
  effect, safe to retry".
- **Status codes** by class: `1xx` informational, `2xx` success, `3xx`
  redirection, `4xx` client error (your request was wrong), `5xx` server error
  (the server broke).
- **Statelessness + retries**: a retry-safe API makes `POST` endpoints
  idempotent (Idempotency-Key) or at least safe-to-replay, because a dropped
  response doesn't tell the client whether the request was processed.

## How it fails (review checklist)

- Missing or wrong `Content-Length` (or not supporting `Transfer-Encoding:
  chunked`) — client and server lose sync on the body.
- `GET` with side effects — breaks caching, prefetching, and link bots.
- Non-idempotent `POST` under retry — duplicate rows when a client times out
  and retries.
- Ignoring caching semantics: `GET` responses are cachable by intermediaries;
  if the body depends on the caller, send `Cache-Control: no-store`.
- Not setting `Content-Type`/`Content-Length` on responses — clients guess and
  mis-parse.
- No server timeouts — a stalled client holds a connection forever.
- Assuming a response body on every status (a `204 No Content` has none).

## Build that proves it

`builds/http-server.md` — write a minimal HTTP/1.1 server on raw sockets in
stdlib Python. Parsing the request line, sending correct status lines and
`Content-Length`, and handling malformed input is the fastest way to internalize
this model.

## Drill

Goal: write an HTTP request by hand over a raw socket and read the exact wire
format the response comes back in.

Steps:
1. stdlib `socket`. In one `python3` session:
   ```python
   import socket
   s = socket.create_connection(("example.com", 80))
   s.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
   data = b""
   while chunk := s.recv(4096):
       data += chunk
   print(data.decode()[:600])
   ```
2. Read the output: first line is the status line (`HTTP/1.1 200 OK`), then
   headers, then a blank line, then the body. You hand-wrote the request line,
   the headers, and the terminating blank line — that is the protocol.
3. Break it: change the version to `HTTP/9.9` and re-run. The server replies
   with an error status (e.g. `505 HTTP Version Not Supported`) — it parsed
   your request line and rejected the version.

Self-check (pass/fail):
- Step 1's output starts with `HTTP/1.1 200 OK`, and the body is separated
  from the headers by a blank line.
- Step 3 returns a `5xx`/error status — you can name the line the server
  rejected (the request line) and why (unknown HTTP version).
- You can hand-write a minimal valid request from memory right after.

Why this matters: every framework sits on this exact byte format; when a client
and server disagree, the fight is over these bytes.

## Further reading
- Sriniously, "Understanding HTTP for backend engineers" (▶5) — https://www.youtube.com/watch?v=a3C1DMswClQ (Sep 27, 2024)
- RFC 9110 (HTTP Semantics) — R. Fielding, M. Nottingham, J. Reschke,
  https://www.rfc-editor.org/rfc/rfc9110 (Jun 2022)
- MDN HTTP overview — https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
