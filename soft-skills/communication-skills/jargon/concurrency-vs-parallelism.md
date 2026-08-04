# Concurrency vs. parallelism

Provenance: AI-drafted

Related: [builds/background-worker.md](../../../builds/background-worker.md), [concepts/real-time-data.md](../../../concepts/real-time-data.md)

Concurrency is *structure* — many tasks interleaved on one CPU, making
progress without waiting on each other (async I/O: one thread juggling 100
requests while each blocks on a database read). Parallelism is *hardware* —
truly simultaneous execution on multiple cores. Python's `asyncio` and
`ThreadPoolExecutor` give concurrency; the GIL blocks CPU-bound parallelism in
one process, so heavy compute goes to `multiprocessing`/ProcessPool.
