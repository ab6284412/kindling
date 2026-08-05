# Scaling databases
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Eric Brewer, PostgreSQL Global Development Group

## What it is

The roadmap's eighth step: what you do when one database instance can't
carry the load — **indexes, sharding, replication, and the CAP theorem**.
This is the theory half of "building for scale" (the practice half lives in
`building-for-scale.md`).

## The concepts

- **Database indexes** — a data structure (B-tree) that makes a lookup fast
  at the cost of write speed and space; the first scaling lever.
- **Sharding strategies** — splitting one table across multiple machines by
  a key (user_id, region, range); scale-out at the cost of joins and
  cross-shard transactions.
- **Data replication** — copies of data on multiple nodes; read replicas
  spread reads, primary/standby gives failover; introduces lag.
- **CAP theorem** — a distributed store can guarantee at most two of
  **Consistency, Availability, Partition tolerance**. Under a network
  partition you must choose: serve stale data (AP) or refuse to serve (CP).

## How it fails (review checklist)

- **Indexing everything** — each index slows writes and eats space; index
  the columns you actually filter/join on, verified by `EXPLAIN`.
- **Sharding before you need it** — a single Postgres with indexes handles
  far more than most apps need; sharding is a last resort with permanent
  complexity (fan-out, hot shards, rebalancing).
- **Replication lag surprises** — read replicas are eventually consistent;
  a "read your own write" page served from a replica can return stale data.
- **CAP as a vibe, not a spec** — CAP is about partitions, not a menu;
  modern systems are "CP during partition, AP otherwise" in practice.

## Build that proves it

No build yet. The drill: explain, for your own API, which CAP corner
Postgres gives you, and sketch a shard key for its biggest table and the
query it breaks.

## Drill

Goal: prove an index changes the query plan — and that the database itself
shows you the proof. Stdlib only (SQLite's `EXPLAIN QUERY PLAN`).

Steps:
1. Save this as `index_drill.py`:
   ```python
   import sqlite3

   c = sqlite3.connect(":memory:")
   c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, email TEXT)")
   c.executemany("INSERT INTO users VALUES (?, ?)",
                 [(i, f"u{i}@x.com") for i in range(10000)])
   c.execute("ANALYZE")

   q = "SELECT * FROM users WHERE email = 'u9999@x.com'"
   print("before index:", c.execute("EXPLAIN QUERY PLAN " + q).fetchone())
   c.execute("CREATE INDEX idx_email ON users(email)")
   print("after index: ", c.execute("EXPLAIN QUERY PLAN " + q).fetchone())
   ```
2. Run `python3 index_drill.py`.

Self-check (pass/fail — run it alone): the plan flips from a table-wide
`SCAN users` to `SEARCH users USING INDEX idx_email`. If the second line still
says `SCAN`, either the index wasn't created or the query isn't using the
indexed column — a real-world signal that your "optimization" isn't being
used. You passed when you can read the two plans and say what changed.

Why this matters: `EXPLAIN` is the database telling you the truth about your
query; an index that never appears in any plan is write-cost with zero read
benefit — measure with `EXPLAIN` before and after, the same way you'd profile
code.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Scaling Databases" step
  (fetched Aug 3 2026)
- Eric Brewer, https://www.cs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf —
  "CAP twelve years later" keynote (fetched Aug 3 2026)
- PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/ — PostgreSQL documentation
  (fetched Aug 3 2026)
