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

## Drill

Goal: write a 10-line router and reproduce the route-order bug and the
wrong-method failure the note warns about.

Steps:
1. stdlib. Save `router.py`:
   ```python
   import re
   routes = [
       ("GET", r"^/items/(\w+)$", "item by id"),   # wildcard FIRST — bug
       ("GET", r"^/items/new$", "new item form"),
   ]
   def handle(method, path):
       for m, pat, name in routes:
           if re.match(pat, path):
               return name if m == method else "405 method not allowed"
       return "404 not found"
   print(handle("GET", "/items/new"))   # bug: wildcard swallows it
   ```
   Run it — `/items/new` prints `item by id`.
2. Swap the list so the specific route comes first and re-run — now it prints
   `new item form`. Order matters: first match wins.
3. Add the method dimension: `("GET", r"^/items$", "list")` and
   `("POST", r"^/items$", "create")`. Then `handle("DELETE", "/items")` must
   print `405 method not allowed` (known path, wrong method) and
   `handle("GET", "/nope")` must print `404 not found`.

Self-check (pass/fail):
- Step 1 prints `item by id` for `/items/new`; after the swap in step 2 it
  prints `new item form`.
- Step 3: `DELETE /items` → `405`, `GET /nope` → `404` — a wrong method is not
  a fall-through to 404.
- You can state the fix for order bugs in one sentence (specific routes before
  wildcards).

Why this matters: order bugs and method-pile routes are the two named failure
modes; a 10-line table reproduces both before they cost you a debug session in
FastAPI.

## Further reading
- Sriniously, "What is Routing in Backend?" (▶6) — https://www.youtube.com/watch?v=SubuU1iOC2s (Dec 9, 2024)