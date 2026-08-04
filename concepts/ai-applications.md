# AI applications (building AI features)
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, OpenAI docs, Anthropic docs

## What it is

The roadmap's "Applications" step — the AI *products* a backend can build
with LLM providers: **prompting techniques, Gemini, OpenAI, Anthropic, and
refactoring** with AI help. The "how to ship AI features" track.

## The concepts

- **Prompting techniques** — engineering the input: system prompts,
  few-shot examples, output formats; still the cheapest lever on output
  quality.
- **Gemini / OpenAI / Anthropic** — the API providers you call from your
  backend; each has a docs/SDK story and different models/pricing/latency.
- **Refactoring** — using AI to restructure code; the safest AI task
  because behavior is (supposed to be) unchanged and tests can verify it.

## How it works

Your backend wraps a provider API: validate input → build the prompt →
call the model → validate output (see `integration-patterns.md` for the
shipping half: streaming, structured outputs, function calling, RAG). The
app's job is to be a *reliable* client of an *unreliable, stochastic*
dependency.

## How it fails (review checklist)

- **Untested AI behavior** — the model is a stochastic dependency; snapshot
  / golden tests on outputs catch regressions.
- **Prompt as product** — prompts drift silently; version them like code.
- **Ignoring provider cost/latency** — each call is money and milliseconds;
  cache, batch, and model-shop (see this workspace's
  `knowledge/time-to-thought.md`, whose embedded drill measures it).
- **Sending secrets/user data to the provider unconsidered** — PII in
  prompts is a data-leak decision; know what leaves your server.

## Build that proves it

The drill embedded in [time-to-thought.md](../knowledge/time-to-thought.md) —
measure TTFT/quality tradeoffs across
models for one task. That's the hands-on rep for this step.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Applications" step (fetched
  Aug 3 2026)
- OpenAI docs, https://platform.openai.com/docs (fetched Aug 3 2026)
- Anthropic docs, https://docs.anthropic.com/en/docs (fetched Aug 3 2026)
