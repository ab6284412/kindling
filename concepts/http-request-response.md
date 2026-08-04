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

## Further reading
- Sriniously, "Understanding HTTP for backend engineers" (▶5) — https://www.youtube.com/watch?v=a3C1DMswClQ (Sep 27, 2024)
- RFC 9110 (HTTP Semantics) — R. Fielding, M. Nottingham, J. Reschke,
  https://www.rfc-editor.org/rfc/rfc9110 (Jun 2022)
- MDN HTTP overview — https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
