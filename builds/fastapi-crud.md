# Build: a CRUD API with FastAPI + raw SQL (no ORM)
Source: `concepts/fastapi-dependency-injection.md`, `dsa/hashing.md`
Provenance: AI-drafted · Credits: Sebastián Ramírez (FastAPI docs)

Goal: construct a full create/read/update/delete API by hand — FastAPI with a
dependency-injected database session and raw SQL, no ORM, so the HTTP layer and
the data layer are both visible and testable.

## Spec

Write `app.py` (stdlib `sqlite3`, no ORM, no third-party DB driver) that:

1. Connects to `todo.db` via a FastAPI dependency `get_db` that yields a
   `sqlite3.Connection`, calls `row_factory = sqlite3.Row` so rows read like
   dicts, and closes the connection when the request ends (try/finally).
2. Creates the table on startup (at import, not per request): `todos(id INTEGER
   PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)`.
3. Exposes exactly:
   - `POST /todos` — body `{"title": str, "done": bool?}` → `201` with the
     created row (return the `lastrowid`, then `SELECT` it back).
   - `GET /todos` → `200`, `[{id, title, done}, ...]`.
   - `GET /todos/{id}` → `200` or `404`.
   - `PATCH /todos/{id}` — partial update of `title`/`done` (only keys
     present) → `200` or `404`.
   - `DELETE /todos/{id}` → `204` or `404`.
4. Every handler runs its SQL through a **parameterized query** (`?` placeholders)
   — string-concatenating user input is a failing grade.
5. Uses a `pydantic.BaseModel` for the POST/PATCH bodies; `done` defaults to
   `False`.

## Constraints

- `sqlite3` from the stdlib only — no SQLAlchemy, no psycopg, no aiosqlite.
- All SQL written by hand inside the endpoints; the app must not import any
  "database" helper besides `sqlite3`.
- `connect()` runs per request via the dependency (the pooling question is an
  extension, not v1).

## Self-check (pass/fail)

Run `uvicorn app:app` (this repo's `web/.venv` has fastapi + uvicorn), then in
order:

```bash
curl -s -X POST localhost:8000/todos -H 'content-type: application/json' \
  -d '{"title":"write build","done":true}' -i   # 201, JSON has id=1
curl -s -X POST localhost:8000/todos -H 'content-type: application/json' \
  -d '{"title":"verify it"}' -i                 # 201, id=2, done=0
curl -s localhost:8000/todos                     # 200, two rows, id order 1,2
curl -s localhost:8000/todos/1                   # 200, title "write build"
curl -s localhost:8000/todos/99                  # 404
curl -s -X PATCH localhost:8000/todos/2 -H 'content-type: application/json' \
  -d '{"done":true}' -i                          # 200, done=1, title unchanged
curl -s -X DELETE localhost:8000/todos/1 -i      # 204, empty body
curl -s localhost:8000/todos                     # 200, exactly one row left
```

Run the suite twice — delete `todo.db` between runs. Both runs must produce
identical output (fresh table each time). Restart uvicorn between runs to prove
state lives in the DB, not the process.

Gotcha to expect: SQLite stores booleans as integers, so `done` comes back as
`1`/`0` in the JSON, not `true`/`false`. That's correct behavior for `sqlite3`
— if the exact booleans matter, coerce `bool(row["done"])` at the response
boundary.

## Extensions (only after the base passes)

- Swap the storage for Postgres: replace `?` with `%s`, `AUTOINCREMENT` with
  `SERIAL`, and `connect` with a `psycopg` connection. The dependency boundary
  means only `get_db` and the SQL dialect change — the endpoints should not.
- Add `GET /todos?limit=&offset=` pagination.
- A `unique` constraint on `title` returning `409` on a duplicate.

## Why this matters

This is the exact shape of a real FastAPI service — dependency-injected DB
session, hand-written SQL, JSON in/out — minus the ORM's magic. When the ORM
later hides a slow query, this build is why you'll know what it's actually
executing.
