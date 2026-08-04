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

## Build that proves it

The transactions drill lives in [transactions-acid.md](transactions-acid.md).
No build yet for N+1: the drill is to write a FastAPI + SQLAlchemy endpoint,
query a list, inspect the SQLAlchemy query log, find the N+1, and fix it with a
join.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "More about Databases" step
  (fetched Aug 3 2026)
- PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/ — PostgreSQL documentation
  (fetched Aug 3 2026)
- SQLAlchemy docs, https://docs.sqlalchemy.org/en/20/ — ORM documentation
  (fetched Aug 3 2026)
