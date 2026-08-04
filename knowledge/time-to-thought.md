# Time-to-thought: the second axis of the model race
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: Martin Alderson

## Summary
Lobsters discussion: "I'm (mostly) picking models on speed now, not intelligence."
For people shipping agents, latency is a feature, not just a cost — time to first
token and wall-clock throughput decide whether a model feels good in a loop.

## Lesson
When you evaluate a model API, measure quality *and* latency. A smarter model
that takes 2x as long can feel worse in an agent loop. Compare on the same
prompt: TTFT, total time, score. Numbers, not vibes.

## Drill
Goal: quantify the speed-vs-quality trade on real model APIs, in numbers.

Steps:
1. FastAPI endpoint `POST /chat` that calls one model provider (any free-tier one).
2. Record time-to-first-token (streamed) and total time (non-streamed).
3. Same prompt against two models: one faster/weaker, one slower/stronger.
4. Score both answers. Chart time vs. score.

Self-check: you can state the TTFT difference in seconds for a concrete pair of
models, and justify which one you'd put in an agent loop.

Why this matters: the people shipping agents pick on latency as often as
quality. If you can't measure it, you're guessing.

## Further reading
- Martin Alderson, https://martinalderson.com/posts/speed-vs-intelligence/ — "I'm (mostly) picking models on speed now, not intelligence" (Aug 2 2026; surfaced on Lobsters/HN)
