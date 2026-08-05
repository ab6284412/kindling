# NoSQL databases
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Redis docs, MongoDB docs

## What it is

The roadmap's sixth step: databases that trade relational normalization for
a specific data shape or access pattern — **document** stores, **key-value**,
**graph**, **columnar**, **time-series**, and **in-memory** caches. The
roadmap lists MongoDB, Redis, DynamoDB, CouchDB, Neo4j, Cassandra, SQLite,
InfluxDB, TimescaleDB, Firebase, RethinkDB, AWS Neptune, ClickHouse,
ScyllaDB, and DGraph.

## The concepts (by shape)

- **Document (JSON):** MongoDB, CouchDB, Firebase, DGraph — schema-flexible
  documents; MongoDB is the default reference point.
- **Key-value:** Redis, DynamoDB, Memcached — O(1) get/put, the caching layer
  (see `caching.md`).
- **Graph:** Neo4j, AWS Neptune — nodes + edges, made for relationship
  traversal.
- **Columnar / wide-column:** Cassandra, ScyllaDB, ClickHouse, DynamoDB —
  analytic/append-heavy workloads.
- **Time-series:** InfluxDB, TimescaleDB — timestamped metrics.
- **Embedded:** SQLite — a file, no server; ubiquitous as the "local" store.
- **Realtime:** RethinkDB, Firebase Realtime Database — push updates to
  clients.

## How it works

NoSQL is a category of *trades*, not one technology. The unifying idea: give
up cross-record joins/ACID guarantees to gain horizontal scaling or
low-latency access at the specific access pattern. Choosing one is choosing
a workload, not "being modern."

## How it fails (review checklist)

- **Choosing NoSQL because it sounds modern** — most apps' data is
  relational; Postgres wins until measured otherwise.
- **Denormalization without a plan** — copying data across documents for
  speed, then watching it drift out of sync.
- **Using Redis as the system of record** — it's a cache; it can lose data
  (see `caching.md`).
- **Schema flexibility = no schema** — you still need validation, now you
  just enforce it in the app.

## Build that proves it

No build yet. The test: for each of the 15 databases above, name its data
shape, one workload it's best at, and one where a relational DB beats it.

## Drill

Goal: reproduce the NoSQL denormalization trap — copied data drifting out of
sync — and contrast it with a relational join. Stdlib only.

Steps:
1. Save this as `drift_drill.py`:
   ```python
   import sqlite3

   # Document store: the user's name is copied into each order (denormalized)
   users = [{"_id": 1, "name": "alice"}]
   orders = [{"_id": 1, "user": "alice", "total": 9.99}]
   users[0]["name"] = "alice (new)"            # canonical update
   print("doc-store order shows:", orders[0]["user"])

   # Relational: same data, joined at read time
   c = sqlite3.connect(":memory:")
   c.execute("CREATE TABLE u(id INTEGER PRIMARY KEY, name TEXT)")
   c.execute("CREATE TABLE o(id INTEGER PRIMARY KEY, user_id INTEGER, total REAL)")
   c.execute("INSERT INTO u VALUES (1,'alice')")
   c.execute("INSERT INTO o VALUES (1,1,9.99)")
   c.execute("UPDATE u SET name='alice (new)' WHERE id=1")
   print("relational join shows:", c.execute(
       "SELECT o.total, u.name FROM o JOIN u ON o.user_id=u.id").fetchone())
   ```
2. Run `python3 drift_drill.py`.

Self-check (pass/fail — run it alone): the doc-store print shows the stale
name (`alice`) while the relational join shows the fresh name
(`alice (new)`) — one source of truth updated, only the denormalized copy
drifted. If both print the same value, your store never actually denormalized
in step 1.

Why this matters: denormalization buys speed and pays in drift; whenever you
copy a field across documents you must decide who owns it and how the copies
get updated — "just copy it" is how invoices start showing yesterday's
username.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "NoSQL Databases" step
  (fetched Aug 3 2026)
- Redis docs, https://redis.io/docs/ (fetched Aug 3 2026)
- MongoDB docs, https://www.mongodb.com/docs/ (fetched Aug 3 2026)
