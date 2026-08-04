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

No build yet. The drill: add `Cache-Control` + `ETag` to one of your
FastAPI endpoints, verify the browser revalidates, then add a Redis cache
for your slowest query and prove the second call skips the DB.

## Further reading
- Sriniously, "Caching, the secret behind it all" (▶13) — https://www.youtube.com/watch?v=estH64OkwxU (Mar 5, 2025)
- roadmap.sh, https://roadmap.sh/backend — "Caching" step (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching —
  "HTTP caching" (fetched Aug 3 2026)
- Redis docs, https://redis.io/docs/ (fetched Aug 3 2026)
