# Search engines (Elasticsearch, Solr)
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Elastic docs, Apache Solr docs

## What it is

The roadmap's search-engine step: full-text search systems that index your
data so users can find it fast — **Elasticsearch** (the default) and
**Solr**. When `WHERE name LIKE '%term%'` won't cut it (fuzzy, ranking,
facets, scale), you add a search engine.

## The concepts

- **Elasticsearch** — an Apache Lucene-based search engine exposed as a
  JSON REST API; inverted indexes, relevance scoring, aggregations;
  scales horizontally; the default choice.
- **Solr** — the older Lucene-based sibling, XML config, still used in
  enterprise search.

## How it works

Instead of scanning tables, the engine builds an **inverted index**: a map
of every term → the documents containing it. Queries then rank matches by
relevance (TF-IDF/BM25), apply analyzers/tokenizers, and aggregate. You
typically feed it from your primary DB (a change-data pipeline), so it is a
*derived* store that can be rebuilt — like a cache, not a system of record.

## How it fails (review checklist)

- **"Search" via SQL `LIKE`** — slow at scale, no ranking, no typo
  tolerance; a search engine is the scaling answer (see
  `scaling-databases.md` for the same logic in DBs).
- **Search engine as the source of truth** — it's a derived index; rebuild
  it from the DB, never hand-edit it.
- **No analyzer awareness** — "chocolate" vs "chocolates" vs "Chocolate"
  behave differently depending on tokenization/stemming; test the mapping.
- **Watching it outgrow the box** — clusters need sharding/replica planning;
  that's `scaling-databases.md`'s CAP tradeoffs again, applied to search.

## Build that proves it

No build yet. The drill: index a small dataset (say 10k rows) into
Elasticsearch running in Docker, then write the queries that return ranked,
fuzzy-tolerant, faceted results — and compare the query time to the same
search in Postgres.

## Further reading
- Sriniously, "Full text search using Elasticsearch" (▶15) — https://www.youtube.com/watch?v=7_sovzAhRSM (Jul 5, 2025)
- roadmap.sh, https://roadmap.sh/backend — "Search Engines" step
  (fetched Aug 3 2026)
- Elastic docs, https://www.elastic.co/docs (fetched Aug 3 2026)
- Apache Solr Guide, https://solr.apache.org/guide/ (fetched Aug 3 2026)
