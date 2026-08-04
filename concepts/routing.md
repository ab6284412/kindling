# Routing
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

Routing maps an incoming request — method + path + host — to the handler that
should answer it. It's the switchboard of a web backend: `GET /items` → "list",
`POST /items` → "create". Sriniously's ▶6 is the dedicated treatment.

## How it works

- The server compares the request target against a table of patterns. Exact
  match, then parameterized segments (`/items/{id}` → capture `id`).
- Extra dimensions constrain the match: HTTP method, host, headers (content
  negotiation), middleware order.
- Order matters: first match wins in most routers, so specific routes come
  before wildcards.

## How it fails

- **Order bugs**: a `/items/{id}` route registered before `/items/new` swallows
  `new` as an id.
- **Overloading path with method**: `/get_item`, `/create_item` instead of
  `GET /items`, `POST /items` — routes become a pile, not a table.
- Ignoring `HEAD`/`OPTIONS`/`404`: every route needs the right method; a wrong
  method should 405, not fall through.
- Trailing-slash and case mismatches that silently 404 or double-up.

## Build that proves it

Build: covered in [builds/http-server.md](../builds/http-server.md) — pattern-match the request
line to handlers on raw sockets; add a `{id}` segment to see capture-by-hand.

## Further reading
- Sriniously, "What is Routing in Backend?" (▶6) — https://www.youtube.com/watch?v=SubuU1iOC2s (Dec 9, 2024)