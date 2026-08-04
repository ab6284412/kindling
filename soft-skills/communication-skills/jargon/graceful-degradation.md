# Graceful degradation

Provenance: AI-drafted

Related: [concepts/building-for-scale.md](../../../concepts/building-for-scale.md), [concepts/caching.md](../../../concepts/caching.md)

The system keeps a useful core when a dependency fails, instead of failing
whole. Serving cached data while the database is down, showing the fallback
image, or demoting a slow feature. It's the answer to "what's the smallest
working version of our product if the third-party API vanishes?" — a capacity
and product question, not just an ops one.
