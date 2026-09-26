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
- **RAG / vectors / embeddings / agents / skills / MCP** — the retrieval
  and tool-calling stack the roadmap files under this step; full treatment
  in [ai-integration-patterns.md](ai-integration-patterns.md).

## How it works

Your backend wraps a provider API: validate input → build the prompt →
call the model → validate output (see `ai-integration-patterns.md` for the
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

## Drill

Goal: prove your app survives a stochastic model — it validates and retries
model output instead of trusting it — using a fake model, stdlib only.

Steps:
1. From a scratch dir, save this as `client.py` and run `python3 client.py`:
   ```python
   import json, re
   calls = 0
   def fake_model(prompt):          # stand-in for an LLM: flaky output
       global calls
       calls += 1
       if calls % 2 == 0:
           return "Sure! " + json.dumps({"sentiment": "positive", "score": 0.9})
       return "Here is the result: not valid json"
   def parse(raw):                  # your reliability layer
       m = re.search(r"\{.*\}", raw, re.S)
       return json.loads(m.group(0))
   def complete(prompt, retries=3): # validate + retry
       for _ in range(retries):
           raw = fake_model(prompt)
           try:
               return parse(raw)
           except (json.JSONDecodeError, AttributeError):
               print(f"[retry] unparseable model output: {raw!r}")
       raise RuntimeError("model kept failing — say so, don't guess")
   print(complete("classify this review"))
   print(f"model calls = {calls} (>=2: we retried, we didn't crash)")
   ```
2. Read the output.
3. Change `retries=1` and rerun.

Self-check (pass/fail — run it alone):
- First run prints `model calls = 2` and the parsed dict — the unparseable
  first attempt was retried, not propagated as a crash.
- With `retries=1` it raises `RuntimeError` — degraded but with a clean
  error, never a bare `json.JSONDecodeError` leaking into your endpoint.
- Swap `fake_model` for your real provider call; the wrapper is unchanged.

Why this matters: an LLM is a probability engine, not a contract — your
app's job is validation, retry, and graceful failure, exactly like any
flaky third-party API.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Applications" step (fetched
  Aug 3 2026)
- OpenAI docs, https://platform.openai.com/docs (fetched Aug 3 2026)
- Anthropic docs, https://docs.anthropic.com/en/docs (fetched Aug 3 2026)
