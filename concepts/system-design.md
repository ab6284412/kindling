# System design
Created 2026-08-06 · Last verified 2026-08-06
Provenance: AI-drafted · Credits: roadmap.sh, Donne Martin (system-design-primer), Hello Interview

## What it is

The roadmap's sibling track (a button to roadmap.sh/system-design, not a step):
given an ambiguously-worded product ("design a URL shortener"), break it into
the pieces of infrastructure that solve it — load balancers, caches, databases,
queues — and reason about the trade-offs. Unlike DSA, there is no single right
answer; the interviewer grades how you navigate the problem, pick components,
and weigh options. Entry-level roles usually skip it; it becomes common at
mid-level and dominant at senior (Hello Interview, 2026).

## The concepts (the trade-offs, then the components)

Everything is a trade-off — no component is free, each adds hardware and
operational complexity.

- **Performance vs scalability** — performance: slow for one user; scalability:
  fast for one user, slow under load. A system is scalable if adding resources
  improves throughput proportionally.
- **Latency vs throughput** — latency is time per action, throughput is actions
  per unit time; aim for maximal throughput at acceptable latency.
- **Availability vs consistency (CAP)** — under a network partition you pick C
  (every read sees the latest write) or A (every request gets an answer, maybe
  stale), never both. CP: atomic reads/writes, may time out. AP: eventually
  consistent, keeps serving.
- **Consistency patterns** — weak (reads may miss writes; memcached), eventual
  (DNS, email), strong (RDBMS, file systems).
- **Availability patterns** — fail-over (active-passive: heartbeat + standby;
  active-active: both serve) and replication (master-slave reads, master-master
  writes). Nines: 99.9% ≈ 8h45m/year downtime, 99.99% ≈ 52min/year.
- **DNS** — name → IP, hierarchical, cached with a TTL; A, CNAME, MX, NS records.
- **CDN** — distributed proxy network serving static content from near the user;
  push (you upload) vs pull (fetched on first request, TTL-bounded).
- **Load balancer** — distributes requests across servers; L4 (IP/port) vs L7
  (HTTP payload, cookies); enables horizontal scaling. It is itself a single
  point of failure — run multiple.
- **Reverse proxy** — a single entry point even for one server: SSL termination,
  compression, caching, hiding backend. NGINX/HAProxy do both proxy + balancing.
- **Application layer / microservices** — separate web from app servers to scale
  independently; stateless servers with sessions in a shared store (Redis);
  service discovery (Consul, etcd, ZooKeeper) registers address + health checks.
- **Database scaling** — replication (read replicas, write to master),
  federation (split DBs by function), sharding (split data across DBs; key on
  something stable, watch hot shards), denormalization (copy data to avoid
  joins, pay in drift), SQL tuning (benchmark + profile the slow query log).
- **Cache** — client, CDN, web-server, DB-query, object-level; update strategies
  cache-aside, write-through, write-behind, refresh-ahead.
- **Asynchronism** — message queues (broker decouples) and task queues (retries,
  prioritization) so a slow consumer doesn't block the producer.
- **Communication** — TCP (reliable, ordered) vs UDP (fast, lossy), RPC
  (call a remote method) vs REST (resources + verbs).
- **Back-of-envelope estimation** — the first pass: users × requests/sec × data
  per request; powers-of-two and latency numbers (network round trip ~ms,
  disk seek ~10ms, memory ~100ns) make or break the estimate.

## How it fails (review checklist)

- **Jumping to components before scoping** — no requirements gathered (who uses
  it, how many users, RPS, read:write ratio), then a design that solves the
  wrong problem. The most common junior failure (Hello Interview, 2026).
- **Memorized answers** — interviewers probe trade-offs on purpose; knowing
  "Redis" but not why beats knowing the answer but not the reasoning.
- **Vertical scaling as the plan** — scale-up on one box is simpler but caps
  out and is a single point of failure; horizontal needs stateless servers.
- **A single load balancer / single cache** — each un-failed-over component is
  a new single point of failure.
- **Sharding on a hot key** — a power-user shard becomes the bottleneck;
  consistent hashing reduces rebalancing pain.
- **Forgetting the numbers** — a design that ignores latency/throughput can't
  be sanity-checked against the load it claims to serve.

## Build that proves it

No build yet. The exercise the primer recommends: whiteboard-design a URL
shortener (or Bit.ly/Pastebin) end-to-end with the steps below — the drill is
the estimation pass; the design is the spoken part.

## Drill

Goal: run the back-of-envelope pass for a URL shortener, then list the
components you'd add at each load step. Stdlib only.

Steps:
1. Save this as `sizing.py` and run `python3 sizing.py`:
   ```python
   DAILY = 10_000_000                     # writes/day (new short URLs)
   READ_PER_WRITE = 100                    # 100:1 read:write is typical
   SECONDS_PER_DAY = 86400
   avg_writes_per_s = DAILY / SECONDS_PER_DAY
   peak_writes_per_s = avg_writes_per_s * 5   # 5x peak factor
   peak_reads_per_s = peak_writes_per_s * READ_PER_WRITE
   row_bytes = 8 + 200 + 500               # id + short url + long url
   storage_per_year = DAILY * row_bytes * 365 / (1024**3)
   print(f"avg {avg_writes_per_s:.0f} writes/s, peak {peak_writes_per_s:.0f} writes/s")
   print(f"peak {peak_reads_per_s:.0f} reads/s -> replicas + Redis before you ship")
   print(f"{storage_per_year:.0f} GB/yr -> one Postgres, plan a shard/archive before year two")
   ```
2. Speak the rest out loud, one minute each: (a) hash or DB-id for the short
   key + collision handling, (b) read path: LB → cache → DB, (c) what breaks
   when peak reads exceed one DB's capacity → add read replicas, then a cache.

Self-check (pass/fail — run it alone):
- The numbers print: ~115 avg writes/s, ~579 peak writes/s, ~57,870 peak
  reads/s, ~2,407 GB/year storage. If your arithmetic disagrees with the
  script's, the script wins — re-derive yours.
- For (b) you named LB, cache, and DB as the three read-path hops.
- For (c) you said read replicas *then* cache (replicas first; a cache fronting
  an already-saturated DB just delays the 503s).

Why this matters: the estimate decides the architecture. ~2.4 TB/yr means "one
Postgres, but plan sharding/archiving before year two"; ~58K reads/s means
"replicas + Redis before you ship." Sizing first is what keeps a design honest.

## Further reading
- roadmap.sh, https://roadmap.sh/system-design — System Design roadmap (fetched Aug 6 2026)
- Donne Martin, https://github.com/donnemartin/system-design-primer — "The System
  Design Primer" (fetched Aug 6 2026)
- Hello Interview, https://www.hellointerview.com/learn/system-design — "System
  Design in a Hurry" (fetched Aug 6 2026)
