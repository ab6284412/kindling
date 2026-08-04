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

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "NoSQL Databases" step
  (fetched Aug 3 2026)
- Redis docs, https://redis.io/docs/ (fetched Aug 3 2026)
- MongoDB docs, https://www.mongodb.com/docs/ (fetched Aug 3 2026)
