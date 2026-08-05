# More about databases
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, PostgreSQL Global Development Group, SQLAlchemy docs

## What it is

The roadmap's seventh step: the database *skills* that separate a person who
can run a query from a backend engineer — **ORMs, normalization, ACID,
failure modes, transactions, performance profiling, and the N+1 problem**.
The ACID and transactions half is already deep-covered in
`transactions-acid.md`.

## The concepts

- **ORMs** — object-relational mappers (SQLAlchemy in this stack) turn
  classes into tables and let you query with Python instead of SQL strings.
- **Normalization** — splitting data into tables so each fact lives once;
  the 1NF→3NF rules; prevents update anomalies.
- **ACID** — atomicity, consistency, isolation, durability; see
  `transactions-acid.md`.
- **Failure modes** — how a DB misbehaves: lock contention, deadlocks,
  bloat, replication lag, connection exhaustion.
- **Transactions** — grouping statements into all-or-nothing units; see
  `transactions-acid.md`.
- **Profiling performance** — `EXPLAIN ANALYZE`, index scans vs. seq scans,
  finding the slow query.
- **N+1 problem** — 1 query for the parents + N for the children; classic
  ORM footgun (details below).

## How it fails (review checklist)

- **N+1 in the ORM:** fetching 100 users then `user.posts` each — 101
  queries. Fix: eager-load / join once. The tell: query count in the logs.
- **ORMs hiding the SQL:** writing Python that's slow *and* unreadable
  because you never look at what it generates; read the emitted SQL.
- **Normalization as dogma:** over-normalizing into 50 tables for a 3-table
  app; correctness first, denormalize with intent later.
- **Profiling before measuring:** "optimizing" queries that aren't slow;
  profile first, then change.

## Migrations

Schema changes need the same discipline as code changes: a versioned, ordered
list of migration files instead of ad-hoc `ALTER TABLE` sessions.

- **Versioned, ordered files** — each migration is a file with a revision id
  and a paired `upgrade` (apply) / `downgrade` (undo); the tool records which
  revisions have run, so the schema is reproducible and reviewable like source
  code, not a pile of one-off statements.
- **The failure mode: schema drift** — dev/prod diverge when someone runs an
  ad-hoc `ALTER TABLE` in one place and not the other; suddenly the same code
  works locally and breaks in prod. Migrations turn "both databases end in the
  same state" into a mechanical guarantee instead of a hope.
- **The tool for this stack** — Alembic, the migration tool for SQLAlchemy
  (FastAPI's ORM): `alembic revision -m "add column"` writes a stub you fill
  in, and `alembic upgrade head` applies all pending revisions in order.
- **Never edit an already-applied migration** — once a revision has run
  anywhere it is history; make the next change as a *new* migration. Editing
  applied files is exactly how drift sneaks back in.

## Build that proves it

The transactions drill lives in [transactions-acid.md](transactions-acid.md).
No build yet for N+1: the drill is to write a FastAPI + SQLAlchemy endpoint,
query a list, inspect the SQLAlchemy query log, find the N+1, and fix it with a
join.

## Drill

Goal: reproduce the N+1 query problem with raw SQL, count the queries, then
collapse it to one JOIN. Stdlib only.

Steps:
1. Save this as `nplus1_drill.py`:
   ```python
   import sqlite3

   c = sqlite3.connect(":memory:")
   c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY)")
   c.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, user_id INTEGER)")
   c.execute("INSERT INTO users VALUES (1),(2),(3)")
   for u in range(1, 4):
       c.execute("INSERT INTO posts VALUES (?, ?)", (u, u))

   counted = {"n": 0}
   c.set_trace_callback(lambda sql, *a: counted.__setitem__("n", counted["n"] + 1))

   users = c.execute("SELECT id FROM users").fetchall()
   for u in users:                                   # N+1 pattern
       c.execute("SELECT id FROM posts WHERE user_id=?", (u[0],)).fetchall()
   print("N+1 query count:", counted["n"])           # 1 + 3 = 4

   counted["n"] = 0
   c.execute("SELECT u.id, p.id FROM users u JOIN posts p ON p.user_id = u.id").fetchall()
   print("JOIN query count:", counted["n"])          # 1
   ```
2. Run `python3 nplus1_drill.py`.

Self-check (pass/fail — run it alone): the loop runs `4` queries (1 for
parents + 3 for children) and the JOIN runs exactly `1`. Any count other than
4-and-1 means your trace counted wrong — and when the same pattern shows up in
your ORM logs with 100 users, that's 101 queries per request.

Why this matters: N+1 is the classic ORM footgun — the loop looks like one
operation but is secretly 101 — and the fix is the same in SQLAlchemy:
eager-load or join once, then verify by watching the query log.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "More about Databases" step
  (fetched Aug 3 2026)
- PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/ — PostgreSQL documentation
  (fetched Aug 3 2026)
- SQLAlchemy docs, https://docs.sqlalchemy.org/en/20/ — ORM documentation
  (fetched Aug 3 2026)
- Alembic docs, https://alembic.sqlalchemy.org/en/latest/tutorial.html — "Alembic
  Tutorial" (fetched Aug 5 2026)
