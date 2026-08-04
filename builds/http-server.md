# Build: a minimal HTTP/1.1 server from raw sockets
Source: `concepts/http-request-response.md`
Provenance: AI-drafted · Credits: R. Fielding, M. Nottingham, J. Reschke (RFC 9110)

Goal: construct the full HTTP request/response model by hand — no framework,
no `http.server`, no third-party package.

## Spec

Write `server.py` in stdlib Python that:

1. Listens on `127.0.0.1:8000`.
2. Parses the request line (`METHOD SP target SP HTTP/version CRLF`) and the
   headers that follow. Anything unparseable → `400 Bad Request`.
3. `GET /` → `200 OK`, `Content-Type: text/plain`, body `hello`.
4. `GET /health` → `200 OK`, body `ok`.
5. `POST /echo` → reads exactly `Content-Length` bytes from the body and
   returns them unchanged (`200 OK`, `text/plain`). Missing/odd length → `411`.
6. Anything else → `404 Not Found`.
7. Every response sends `Content-Length` (no chunked encoding in v1) and a
   blank line after the headers.
8. `Connection: close` — handle one request per connection in v1 (keep-alive is
   the extension).

## Constraints

- stdlib only: `socket`, `threading` (optional), nothing else.
- No `http.server`, no `http.client` imports in `server.py`.
- Sequential accept loop is fine for v1; add threads as an extension.

## Self-check (pass/fail)

Run the server, then every line must behave exactly as shown:

```bash
curl -i http://127.0.0.1:8000/            # HTTP/1.1 200 OK, body "hello"
curl -i http://127.0.0.1:8000/health      # 200 OK, body "ok"
curl -i http://127.0.0.1:8000/nope        # 404 Not Found
curl -i -X POST -d "ping" http://127.0.0.1:8000/echo   # 200 OK, body "ping"
curl -i -X GET  http://127.0.0.1:8000/echo             # 411 Length Required
printf 'GARBAGE\r\n\r\n' | nc 127.0.0.1 8000           # 400 Bad Request
```

Each `curl -i` response must include a correct `Content-Length` and a blank
line before the body. A `| nc` check must not hang.

## Extensions (only after v1 passes)

- Keep-alive: loop on one connection until the client closes; honor
  `Connection: keep-alive` and multiple requests per connection.
- `Transfer-Encoding: chunked` response on `GET /` when the client asks.
- Threads: accept loop hands each connection to a thread.
- A timeout on socket reads so a stalled client can't pin the loop forever.

## Why this matters

Every web framework hides this layer. Building it once makes "status codes",
"Content-Length", and "why is the body corrupted" concrete instead of abstract
— and it's the same skill you need to debug a real server at 3am.
