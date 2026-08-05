# Message brokers
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, RabbitMQ docs, Apache Kafka docs

## What it is

The roadmap's fourteenth step: middleware that lets services communicate by
**exchanging messages asynchronously** instead of calling each other
synchronously. The roadmap names **RabbitMQ** (recommended) and **Kafka**.

## The concepts

- **RabbitMQ** — a message broker with queues and exchanges; one producer
  publishes, a worker consumes, the broker guarantees delivery (ack/fail/
  requeue). Best for **task queues** and request/response-style async work.
- **Kafka** — a distributed append-only log; consumers read from offsets
  and can replay. Best for **event streams**, high throughput, and "every
  team subscribes to the same events."

## How it works

Producer → broker → consumer. The producer never waits for the consumer;
the consumer picks work up when it can. This decouples services in time
(no dependency on availability) and in rate (a burst is buffered, not
dropped). RabbitMQ *pushes* work; Kafka has consumers *pull* from an offset
log, which is why Kafka can replay.

## How it fails (review checklist)

- **Broker as a god-object** — routing everything through the broker makes
  it the bottleneck and the single point of failure; use it where async
  genuinely helps.
- **At-least-once vs exactly-once confusion** — brokers deliver at-least-
  once; consumers must be **idempotent** or you'll process duplicates.
- **Unbounded queues** — messages pile up when consumers fall behind;
  monitor queue depth, set TTLs/dead-letter queues.
- **Synchronous-mental-model code** — fire-and-forget publish without
  handling broker failures silently loses work; publishers need retries/
  dead-letter too.
- **Choosing RabbitMQ for streams or Kafka for tasks** — both work, but
  each is tuned for the other's weakness.

## Build that proves it

Proven by [builds/background-worker.md](../builds/background-worker.md). The drill:
run RabbitMQ in Docker, publish a message, consume it in a worker, then kill
the consumer mid-job and prove the message is redelivered (the at-least-once
behavior).

## Drill

Goal: prove the producer→queue→consumer handoff with stdlib `queue.Queue` —
the producer finishes before the consumer even starts.

Steps:
1. From a scratch dir, save this as `handoff.py` and run `python3 handoff.py`
   (stdlib only):
   ```python
   import queue, threading, time
   q = queue.Queue()
   def consumer():
       print("consumer: started", flush=True)
       while True:
           item = q.get()
           time.sleep(0.2)          # pretend each job takes work
           print(f"consumer: did job {item}", flush=True)
           q.task_done()
   threading.Thread(target=consumer, daemon=True).start()
   time.sleep(0.3)                  # let the consumer boot first
   for i in range(5):
       q.put(i)
   print("producer: queued 5 jobs and finished", flush=True)
   q.join()
   print("producer: all jobs acknowledged", flush=True)
   ```
2. Read the output: the producer's "queued 5 jobs and finished" line appears
   *before* the consumer's first "did job 0" — production and consumption
   are decoupled in time.
3. Add a second consumer thread (duplicate the `Thread`/`consumer` lines) and
   rerun: jobs now split across workers, proving you add consumers without
   touching the producer.

Self-check (pass/fail — run it alone):
- Step 1 prints "queued 5 jobs and finished" before any "did job" line, and
  "all jobs acknowledged" last.
- Step 3 prints two interleaved "consumer:" lines sharing the same 5 jobs —
  work is pulled, not assigned.

Why this matters: the broker's whole point is decoupling; this is the same
shape as a RabbitMQ task queue, where a fast producer must never block on a
slow worker.

## Further reading
- Sriniously, "Task queues and background jobs" (▶14) — https://www.youtube.com/watch?v=r-nQsyguU1Y (Apr 16, 2025)
- roadmap.sh, https://roadmap.sh/backend — "Message Brokers" step
  (fetched Aug 3 2026)
- RabbitMQ docs, https://www.rabbitmq.com/tutorials — "RabbitMQ Tutorials"
  (fetched Aug 3 2026)
- Apache Kafka documentation, https://kafka.apache.org/documentation/
  (fetched Aug 3 2026)
