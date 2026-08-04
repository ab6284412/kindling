# AI-assisted coding
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Anthropic docs, GitHub Docs

## What it is

The roadmap's AI-assisted-coding step: how LLM tools fit into a developer's
daily work — **AI code editors and assistants (Claude Code, Copilot, Cursor,
Antigravity), how LLMs work, AI vs traditional coding, code review, and
documentation generation**.

## The concepts

- **Claude Code / Copilot / Cursor / Antigravity** — the assistant tools:
  inline completion and agentic edit-refactor-test loops inside your editor
  or terminal.
- **How LLMs work** — next-token prediction at scale: an LLM is a
  probability engine over tokens, not a search engine over code; it
  *predicts*, so it confidently invents when uncertain.
- **AI vs traditional coding** — traditional code is deterministic and
  auditable; AI-generated code is statistical and must be *reviewed as if
  written by a junior who sounds confident*.
- **Code reviews** — the human gate: check AI output for logic, security,
  and style (see this workspace's `knowledge/retype-generated-code.md` drill).
- **Documentation generation** — AI writes your docstrings/docs from code;
  review, don't trust.

## How it works

Treat the tool as a fast, confident pair programmer: give it a tight spec,
get a draft, **read and verify it**, test it. The skill isn't prompting —
it's the review. This workspace's `knowledge/retype-generated-code.md` drill
practices exactly that: retype/verify code you didn't write.

## How it fails (review checklist)

- **Trusting output unverified** — plausible-looking code with a subtle bug
  is the dangerous case; tests are the safety net (see `testing.md`).
- **No context given** — the model can't fix what you don't describe;
  paste the error, the file, the expected behavior.
- **Copy-paste without understanding** — you are accountable for the code
  that ships under your name; if you can't explain it, don't merge it.
- **Cargo-culting the tool's choices** — AI loves over-engineering; the
  ponytail ladder applies to its output too.

## Build that proves it

The `## Drill` in [retype-generated-code.md](../knowledge/retype-generated-code.md) —
take AI-generated code, find its
failure modes by reading it, and fix them from a spec.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "AI Assisted Coding" step
  (fetched Aug 3 2026)
- Anthropic docs, https://docs.anthropic.com/en/docs (fetched Aug 3 2026)
- GitHub Docs, https://docs.github.com/en/get-started — GitHub Copilot
  coverage (fetched Aug 3 2026)
