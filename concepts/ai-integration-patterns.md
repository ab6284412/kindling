# AI integration patterns
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Anthropic docs, OpenAI docs, Model Context Protocol docs

## What it is

The roadmap's integration-patterns step — the *reliable* ways to connect a
backend to LLMs: **streaming, structured outputs, function calling,
retrieval (RAG, vectors, embeddings), and agent tooling (MCP, skills,
agents)**.

## The concepts

- **Streaming** — return tokens as they're generated (SSE/TCP) so the user
  sees progress instead of waiting for the whole answer.
- **Structured outputs** — make the model return validated JSON/shape
  (constrained decoding or schema-validated post-processing) so your code
  can parse it safely.
- **Function calling** — the model emits a *call* to a function you define;
  your code executes it and feeds results back. The primitive behind agents.
- **Embeddings** — turn text into a vector so "similarity" becomes vector
  distance; the input to RAG.
- **Vectors** — the representation and the storage (pgvector, vector DBs).
- **RAGs (retrieval-augmented generation)** — fetch relevant documents
  first (via embeddings), stuff them into the prompt, so the model answers
  from *your* data instead of its training. Grounds answers, cuts
  hallucination, adds provenance.
- **MCP (Model Context Protocol)** — an open protocol for giving models
  access to tools/data sources; how agents reach external systems.
- **Skills / Agents** — skills are packaged capabilities; agents are loops
  (model → tool call → observation → next step) that act until done.

## How it works

The through-line: LLMs are unstructured and stochastic, so *you* add the
structure — validate inputs, constrain outputs, ground answers in
retrieved data, and turn reasoning into callable functions. Every pattern
here is a way of making a probability machine behave like a contract.

## How it fails (review checklist)

- **Raw model output parsed as JSON** — one stray token breaks it; use
  structured outputs or validate+retry.
- **RAG without evaluation** — retrieval quality is a metric, not a vibe;
  test top-k relevance before trusting answers.
- **Agents without guardrails** — an agent loop can call tools in a loop,
  spend money, or do damage; cap iterations and scope tool permissions.
- **Streaming as an afterthought** — long generations feel dead without it;
  latency UX matters (see `knowledge/time-to-thought.md`).

## Build that proves it

No build yet. The drill: one endpoint that streams a model's answer, with
the prompt constructed from an embedding search over a small document set
(RAG), and a structured-output JSON contract on the reply.

## Drill

Goal: prove you can turn raw, unpredictable model output into a validated
JSON contract — stripping fences, tolerating prose — stdlib only.

Steps:
1. From a scratch dir, save this as `parse.py` and run `python3 parse.py`:
   ```python
   import json, re
   bt = chr(96)   # a backtick, built at runtime so it can't close this code fence
   samples = [
       '{"name": "Ada", "age": 36}',                                # clean
       bt * 3 + 'json\n{"name": "Bob", "age": 41}\n' + bt * 3,      # fenced
       'Here you go: {"name": "Cy", "age": 29} hope that helps',    # prose around
       bt * 3 + 'json\n{"name": "not-quite',                        # broken doc
   ]
   def extract(raw):
       m = re.search(r"\{.*\}", raw, re.S)   # first {...} block
       if not m:
           raise ValueError(f"no JSON in: {raw!r}")
       return json.loads(m.group(0))
   def validate(d):
       assert isinstance(d.get("name"), str), "name must be str"
       assert isinstance(d.get("age"), int), "age must be int"
       return d
   for s in samples:
       try:
           print("OK  ", validate(extract(s)))
       except (ValueError, json.JSONDecodeError, AssertionError) as e:
           print("BAD ", s[:28], "->", e)
   ```
2. Read the output.

Self-check (pass/fail — run it alone):
- The first three samples print `OK` with the parsed dict — fences and
  surrounding prose are handled, and the same parser works on all of them.
- The last sample prints `BAD ... -> no JSON in: ...` — it's rejected with a
  clear error, and you can retry (see the `ai-applications.md` drill) instead
  of crashing.
- Add `'{"name": "Dan", "age": "thirty-six"}'` as a sample: it prints
  `BAD` via the `assert` — a wrong-typed field never reaches your code as an
  int.

Why this matters: "the model returns JSON" is a lie until you've parsed and
validated it — structured outputs exist to turn that lie into a contract
your endpoint can depend on.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Integration Patterns" step
  (fetched Aug 3 2026)
- Model Context Protocol docs, https://modelcontextprotocol.io/ (fetched
  Aug 3 2026)
- OpenAI docs, https://platform.openai.com/docs (fetched Aug 3 2026)
- Anthropic docs, https://docs.anthropic.com/en/docs (fetched Aug 3 2026)
