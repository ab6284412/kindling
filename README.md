# Tech Research & Learning Lab

A research + learning workspace for junior backend developers. It turns the
daily AI/dev-tools news cycle into a repeatable habit: **pull → verify → distill
→ practice**. Every news item becomes either a transferable lesson or a drill,
and fundamentals are covered by a structured free curriculum.

Built with no dependencies: `pull.py` is stdlib-only, notes are markdown, and
the "tests" are pass/fail self-checks you run alone.

## The philosophy

The whole system exists to enforce three rules:

1. **We learn, not just summarize.** Every piece of research must produce a
   transferable lesson (a principle, a failure class, a skill) — not a recap.
2. **Separate marketing from substance.** AI companies cherry-pick numbers.
   When a claim looks too clean, ask: what is the denominator? What is being
   hidden? State both the claim and the caveat.
3. **Sources first.** Primary source before secondary commentary, always. A
   note without a source URL and a date is not a note; it's a rumor.

## What's inside

Three pillars, one loop:

1. **Concepts** (`concepts/`) — the textbook. One article per concept a backend
   dev must understand, each traceable to human sources.
2. **Builds + drills** (`builds/`, plus a `## Drill` section inside each
   concept/knowledge note) — the lab. Builds are full-concept, hand-made
   projects; drills are short lesson-specific reps.
3. **News** (`notes/` + `news-ledger.md`) — the current-events pillar. Daily
   digests that report *and* forecast; news signals get scored against reality.

```
pull.py                # news puller: HN, Lobsters, Anthropic, Algolia fallback
                       #   digest subcommand: auto-summarize w/ local Ollama nano model
tests/                 # offline regression tests for pull.py (live HTML fixtures)
notes/                 # dated daily digests — these ROT, read once
knowledge/             # evergreen news-lessons — the compounding part
concepts/              # systematic concept articles (the textbook)
builds/                # hand-made, full-concept exercises
                       # drills live as ## Drill sections inside concepts/knowledge
verify.py              # offline verification: build/stage checks, link check, drill-audit
verify/checks/         # per-build check scripts (run against solutions/<name>)
solutions/             # reference implementations, one per build (checked by verify.py)
dsa/                   # interview prep: patterns-first DSA notes (roadmap-ordered)
soft-skills/           # communication, review, debugging discipline
                       #   communication-skills/jargon/: one term per file
dsa/
  puzzles/             # interview puzzles with answers and self-checks
learning.md            # the structured free curriculum + progress checkboxes
news-ledger.md          # the news ledger (news → trend signals → scored)
followups.md           # standing tracker: what to re-test before citing again
templates/             # skeletons for every artifact type
CONTRIBUTING.md        # how to add a note, concept, build, or news signal
```

The maps: `knowledge/README.md` (lesson → drill → stage) and
`concepts/README.md` (concept → build). Drills are `## Drill` sections inside
the concept/knowledge note that owns them.

## The web study portal (`web/`)

A local FastAPI app that turns this corpus into a study site: browse every
markdown file, tick learning-path stages, mark drills done, reveal drill
self-checks, and attach notes. Content stays read-only — your progress and
notes live in `state.json` (created on first change, gitignored).

```sh
python3 -m venv web/.venv
web/.venv/bin/pip install -r web/requirements.txt
web/.venv/bin/uvicorn web.app:app --reload     # then open http://127.0.0.1:8000
```

Routes: `/` dashboard, `/learning` stages, `/concepts` `/knowledge`
`/notes` `/builds` `/dsa` `/soft-skills` `/content` list pages,
`/news`, `/content/<path>` generic renderer, `POST /api/toggle` and
`POST /api/note` (vanilla-JS, no reloads). Deps (`fastapi`, `uvicorn`,
`jinja2`, `markdown`) are scoped to the app — the no-dependencies rule still
holds for `pull.py` and the content. Tests:
`web/.venv/bin/python -m unittest discover -s tests`.

## Provenance

This workspace is open that AI drafted much of it, because **AI makes
mistakes**. Every content file carries a `Provenance:` mark — `AI-drafted` or
`Human-written` — and a `Credits:` line naming the human author(s) of its
sources. Rule of thumb:

- `AI-drafted` = read the `## Further reading` before you trust the `## Summary`.
- `Human-written` = the file's author vouches for it, with sources to prove it.
- Credits are always given: an article summarized here without its author named
  is a misattribution, not a summary.

## The daily ritual (~20 min)

1. `python3 pull.py digest` — seed a digest auto-summarized by a local Ollama
   nano model (`llama3.2:1b`, no API/auth). Writes `notes/<date>-news-digest.md`.
   If Ollama isn't running it falls back to raw headlines. (Plain `python3
   pull.py` still prints the raw digest to stdout.)
2. **Verify before citing** — a headline is discussed, not necessarily true.
   Check the source and the date; credit the author.
3. Distill: for each item, write the transferable lesson — or skip the item.
4. If a lesson can be practiced, write/extend a drill.
5. For each item that signals a trend, add a row to `news-ledger.md` (one
   falsifiable sentence, one "based on" source).
6. Update `followups.md` with anything new that needs re-testing.

Run the regression check with `python3 -m unittest discover -s tests`.
## Scope & adapting it to you

This repo ships scoped to a **junior backend developer (FastAPI/Python)**.
That assumption is baked into the examples, drills, and `learning.md`. To make
it yours:

- Copy `templates/learner-profile.md` to `PROFILE.md` and edit it.
- Swap `learning.md` stages for your stack.
- Retype the drills you keep — the retyping *is* the learning.

## The system is the product

41 concept notes across 7 learning stages (each with an embedded drill), 7
hand-built projects in builds/ with reference solutions and automated checks,
and a handful of news notes ship today. That's on purpose:
the value is the *machine* — the workflow, templates, and the
concept↔build↔drill↔news-signal wiring — not the current content. Students grow
the content by contributing, and contributing is itself a drill. See
CONTRIBUTING.md.

## License

MIT. See [LICENSE](LICENSE). Content rule of thumb: the process is the product;
attribute sources, don't claim notes you didn't write.
