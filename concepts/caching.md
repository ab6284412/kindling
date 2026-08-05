# Caching
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Mozilla Contributors, Redis docs

## What it is

The roadmap's tenth step: the single highest-leverage performance technique
— keep a copy of an expensive answer somewhere fast so you don't recompute
it. The roadmap names **HTTP caching** (browser/CDN layer) and the cache
servers **Redis** and **Memcached** (app layer).

## The concepts

- **HTTP caching** — cache headers (`Cache-Control`, `ETag`,
  `Last-Modified`) tell browsers and CDNs what may be cached and for how
  long; the cheapest cache of all because it never touches your server.
- **Redis** — in-memory key-value store with rich types; the standard
  app-level cache *and* a pub/sub, rate-limiter, session store (see
  `nosql-databases.md`). Recommended on the roadmap.
- **Memcached** — the original in-memory cache; simpler (plain key-value,
  no persistence), still fine where Redis is overkill.

## How it works

Three layers, three knobs: **HTTP cache** (headers → browser/CDN), **app
cache** (Redis → skip the DB), **DB cache** (indexes/buffer pool → skip the
scan). Each layer trades freshness for speed; invalidation is the hard part,
not the caching.

## How it fails (review checklist)

- **Cache invalidation as an afterthought** — the two hardest problems in CS
  jokes exist because people cache first and think about invalidation never.
- **Caching in Redis, losing the source of truth** — Redis is
  best-effort/persist-if-configured; write-through or store to DB and let
  Redis be a fast copy, not the only copy.
- **No expiry (or absurd TTLs)** — stale data forever, or cache churn.
- **Ignoring the HTTP layer** — the browser round-trip is the slowest part;
  fix `Cache-Control` before adding a Redis cluster.
- **Negative caching forgotten** — cache the expensive miss too, else the
  cache dies under a cache-storm of empty lookups.

## Build that proves it

The storage-cache build proves the cache-with-invalidation half —
[builds/storage-cache.md](../builds/storage-cache.md) (a cache layer whose writes
stay coherent, evicted on every write). A real Redis cache — add one for your
slowest query and prove the second call skips the DB — remains an extension
there.

## Drill

Goal: prove cache hits skip recomputation, that invalidation (`cache_clear`)
is what keeps a stale value fresh, and that eviction drops the oldest entry.
Stdlib only (`functools.lru_cache`).

Steps:
1. Save this as `cache_drill.py`:
   ```python
   from functools import lru_cache

   source = {"price": 10}
   calls = 0

   @lru_cache(maxsize=2)
   def get_price():
       global calls
       calls += 1
       return source["price"]

   print(get_price(), "calls:", calls)        # miss -> 1
   print(get_price(), "calls:", calls)        # hit  -> still 1
   source["price"] = 12                        # source of truth changes
   print("after truth change:", get_price(), "calls:", calls)  # STALE
   get_price.cache_clear()                     # invalidation
   print("after invalidate:", get_price(), "calls:", calls)    # fresh -> 2

   @lru_cache(maxsize=2)
   def slow(k):
       return k * 10
   for k in range(4):
       slow(k)                                # 4 distinct keys, cap of 2
   print("after 4 keys:", slow.cache_info())  # currsize=2, misses=4
   slow(0)                                    # key 0 was evicted -> miss again
   print("after re-get 0:", slow.cache_info())  # misses becomes 5
   ```
2. Run `python3 cache_drill.py`.

Self-check (pass/fail — run it alone): the second `get_price()` call leaves
`calls` at 1 (hit), the value stays `10` even after the source changes to 12
(stale), and only after `cache_clear()` does it return `12` with `calls` at 2.
The eviction proof is `cache_info()`: after 4 keys with `maxsize=2`,
`currsize` is capped at 2 — and re-getting key 0 increments `misses` from 4 to
5, proving it was dropped from the cache. If `calls` ever increments on a
repeated key, your cache isn't caching.

Why this matters: caching is easy; invalidation is the hard half — a stale
price cached forever is worse than no cache, and this is the same miss/hit/
evict logic Redis runs under a different API.

## Further reading
- Sriniously, "Caching, the secret behind it all" (▶13) — https://www.youtube.com/watch?v=estH64OkwxU (Mar 5, 2025)
- roadmap.sh, https://roadmap.sh/backend — "Caching" step (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching —
  "HTTP caching" (fetched Aug 3 2026)
- Redis docs, https://redis.io/docs/ (fetched Aug 3 2026)
