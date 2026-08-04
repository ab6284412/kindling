# Relational databases
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, PostgreSQL Global Development Group

## What it is

The roadmap's fifth step: the database that stores your app's data in
**tables** with **rows and columns**, enforces relationships between tables
(foreign keys), and queries them with **SQL**. The roadmap names
PostgreSQL (recommended), MySQL, MS SQL, Oracle, and MariaDB.

## The concepts

- **PostgreSQL** — open-source, standards-compliant, richest feature set;
  the workspace's stack. Personal recommendation.
- **MySQL** — the most widely deployed open-source RDBMS; the "good enough,
  everywhere" option.
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

No build yet. This workspace's stage 2 (freeCodeCamp Relational Database
cert) is the deep practice.

## Further reading
- Sriniously, "Mastering Databases with Postgres" (▶12) — https://www.youtube.com/watch?v=F7Vwp2Xo5Do (Mar 3, 2025)
- roadmap.sh, https://roadmap.sh/backend — "Relational Databases" step
  (fetched Aug 3 2026)
- PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/ — PostgreSQL documentation
  (fetched Aug 3 2026)
