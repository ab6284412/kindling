# Backpressure

Provenance: AI-drafted
Credits: roadmap.sh, RabbitMQ docs, Apache Kafka docs

Related: [concepts/message-brokers.md](../../../concepts/message-brokers.md), [builds/background-worker.md](../../../builds/background-worker.md)

What a system does when it can't keep up with incoming work: instead of
growing its queue (and memory) forever, it pushes the "I'm full" signal
upstream so the producer slows down or drops. Queues absorb bursts; backpressure
is the rule that a queue must have a limit.
