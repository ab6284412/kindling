# Tail latency

Provenance: AI-drafted

Related: [concepts/building-for-scale.md](../../../concepts/building-for-scale.md), [builds/production-deploy.md](../../../builds/production-deploy.md)

The worst few responses in a distribution, not the average. If a service's p99
is 800ms but p50 is 20ms, the *tail* is what users on slow paths feel — and in a
fan-out (one request hits 20 services), the p99s multiply: 20 services at 5%
slow each makes most requests hit at least one slow leg. Teams optimize p99,
not the mean.
