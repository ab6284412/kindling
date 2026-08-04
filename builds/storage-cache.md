# Build: state & storage — Postgres + a coherent cache
Source: [concepts/relational-databases.md](../concepts/relational-databases.md), [concepts/transactions-acid.md](../concepts/transactions-acid.md),
[concepts/caching.md](../concepts/caching.md), and Sriniously's playlist videos ▶12 (Postgres), ▶13
(Caching), ▶15 (Elasticsearch)
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

Goal: move the CRUD API's storage from SQLite to Postgres and add a cache layer
whose writes stay coherent with the database — proving state lives outside the
process and caches without invalidation are worse than no cache.

## Spec

1. **Postgres swap** — replace `sqlite3` with `psycopg` in `get_db`. Dialect
   changes only: `?` → `%s`, `INTEGER PRIMARY KEY AUTOINCREMENT` →
   `SERIAL PRIMARY KEY`, `INTEGER NOT NULL DEFAULT 0` → `BOOLEAN DEFAULT FALSE`.
   The endpoint logic does **not** change.
2. **Transactions** — a write that spans two steps (e.g. create a todo *and*
   append an `audit_log` row) must be atomic: if step 2 fails, step 1 rolls
   back. Use a single commit after both statements, and prove the rollback in
   self-check.
3. **Cache** — an in-process `dict` keyed by `todo_id`, consulted on
   `GET /todos/{id}`. On a miss, load from Postgres and populate.
4. **Invalidation** — `PATCH /todos/{id}` and `DELETE /todos/{id}` evict that
   id from the cache **after the transaction commits** (never before, or a
   rolled-back write leaves stale-but-valid-looking data). `POST /todos` does
   not populate the cache (new id).
5. A `UNIQUE` constraint on `title` returns `409` on a duplicate.

## Constraints

- `psycopg` + stdlib only. No SQLAlchemy, no Redis (the cache is a plain dict;
   a real KV store is an extension). All SQL written by hand.
- Connect per request via the dependency; the pooling question is an extension.
- Cache eviction happens in the same request as the write, after commit.

## Self-check (pass/fail)

Run Postgres locally (`docker run --rm -e POSTGRES_PASSWORD=p -p 5432:5432
postgres:16`), point `DATABASE_URL` at it, run uvicorn, then:

```bash
curl -s -X POST localhost:8000/todos -H 'content-type: application/json' \
  -d '{"title":"first"}' -i            # 201, id matters
curl -s localhost:8000/todos/1 -i      # 200 (cache miss → DB)
curl -s localhost:8000/todos/1        # 200 (cache hit — same content)
curl -s -X PATCH localhost:8000/todos/1 -H 'content-type: application/json' \
  -d '{"done":true}' -i                # 200
curl -s localhost:8000/todos/1        # 200, done=true (PATCH invalidated cache)
curl -s -X DELETE localhost:8000/todos/1 -i   # 204
curl -s -i localhost:8000/todos/1             # 404 (DELETE evicted it)
```

- **Restart proof**: after restart, `GET /todos/{id}` still returns data —
  it lives in Postgres, not the process (▶12).
- **Rollback proof**: trigger the audit-step failure (e.g. a CHECK constraint
  violation) and show one `SELECT * FROM todos` where the todo row did not
  appear — the statement pair committed atomically or not at all.
- Add a `db-only` turn (a flag that disables the cache); the same curl sequence
  returns identical values. The only differences may be latency.

## Extensions (only after v1 passes)

- Real Redis cache with TTL, cache-aside vs write-through (▶13).
- Connection pooling (`psycopg_pool`) and generous sizing.
- Read replicas for `GET`-heavy routes.

## Why this matters

"Works on my machine" dies the moment the process restarts — persistent state
has to live in a DB, not memory. And a cache that returns stale data after a
write is _worse_ than no cache; invalidation is the part that actually
separates good from broken.