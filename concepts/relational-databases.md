# Relational databases
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, PostgreSQL Global Development Group

## What it is

The roadmap's fifth step: the database that stores your app's data in
**tables** with **rows and columns**, enforces relationships between tables
(foreign keys), and queries them with **SQL**. The roadmap names
PostgreSQL (recommended), MySQL, SQLite, MS SQL, Oracle, and MariaDB.

## The concepts

- **PostgreSQL** — open-source, standards-compliant, richest feature set;
  the workspace's stack. Personal recommendation.
- **MySQL** — the most widely deployed open-source RDBMS; the "good enough,
  everywhere" option.
- **SQLite** — embedded, zero-config, one file, no server; not for
  concurrent production traffic, but the fastest way to prototype and the
  engine every stdlib drill in this workspace uses.
- **MariaDB** — a MySQL fork, drop-in compatible, community-maintained.
- **MS SQL Server** — Microsoft's enterprise RDBMS (T-SQL dialect).
- **Oracle** — legacy enterprise incumbent, expensive, still everywhere in
  banks/ERP.

## How it works

Data is normalized into tables; a schema (columns + types + constraints) is
enforced by the database, not the app. Queries join tables at read time.
Contrast with NoSQL (`nosql-databases.md`): relational = schema-first and
ACID-friendly, the default choice for most business data.

## How it fails (review checklist)

- **Schema as an afterthought** — no types/constraints means garbage data
  you'll clean up forever.
- **N+1 queries** (see `more-about-databases.md`) — a row of code that
  issues one query per parent row.
- **Doing joins in Python** instead of SQL — slower, more code, race-prone.
- **Missing indexes** — full table scans as the table grows.

## Build that proves it

The storage-cache build proves it — [builds/storage-cache.md](../builds/storage-cache.md).
This workspace's stage 5 (freeCodeCamp Relational Database cert) is the deep
practice.

## Drill

Goal: prove foreign keys and constraints are enforced by the database, not the
app — and that the same bad write succeeds when enforcement is off. Stdlib
only.

Steps:
1. Save this as `fk_drill.py`:
   ```python
   import sqlite3

   c = sqlite3.connect(":memory:")
   c.execute("PRAGMA foreign_keys=ON")
   c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
   c.execute("""CREATE TABLE orders(
       id INTEGER PRIMARY KEY,
       user_id INTEGER REFERENCES users(id),
       total REAL)""")
   c.execute("INSERT INTO users VALUES (1, 'alice')")

   try:
       c.execute("INSERT INTO orders VALUES (1, 999, 10.0)")  # no user 999
       print("BAD: orphan order accepted")
   except sqlite3.IntegrityError:
       print("GOOD: orphan order rejected")

   c.execute("INSERT INTO orders VALUES (1, 1, 10.0)")
   print(c.execute(
       "SELECT o.total, u.name FROM orders o JOIN users u ON o.user_id = u.id"
   ).fetchone())
   ```
2. Run `python3 fk_drill.py`.
3. Remove the `PRAGMA foreign_keys=ON` line and re-run.

Self-check (pass/fail — run it alone): with the pragma on, the orphan insert
prints `GOOD: orphan order rejected` and the join returns `(10.0, 'alice')`;
with the pragma off, the orphan insert *succeeds* and the join shows no row
for it — the same app code, different integrity. You passed when you can say
why the constraint belongs in the schema, not in your Python.

Why this matters: schema-first enforcement is the database doing its one job —
constraints catch bad data at the trust boundary, where the app layer would
just silently store it.

## Further reading
- Sriniously, "Mastering Databases with Postgres" (▶12) — https://www.youtube.com/watch?v=F7Vwp2Xo5Do (Mar 3, 2025)
- roadmap.sh, https://roadmap.sh/backend — "Relational Databases" step
  (fetched Aug 3 2026)
- PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/ — PostgreSQL documentation
  (fetched Aug 3 2026)
