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

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Scaling Databases" step
  (fetched Aug 3 2026)
- Eric Brewer, https://www.cs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf —
  "CAP twelve years later" keynote (fetched Aug 3 2026)
- PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/ — PostgreSQL documentation
  (fetched Aug 3 2026)
