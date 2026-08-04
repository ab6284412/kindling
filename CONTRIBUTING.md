# Contributing

Contributing *is* the drill: the fastest way to learn a topic is to write the
knowledge note and the drill for it. Small, focused PRs are the norm here.

## What's welcome

1. **Knowledge notes** — a news lesson distilled with a real source.
2. **Drills** — written as a `## Drill` section inside the concept or knowledge
   note that owns the lesson; a lesson without a drill is a summary, add one and
   it's a skill.
3. **Concept articles** — one concept, one article, traceable to human sources
   (see `concepts/`). This is the "textbook" pillar; the fastest high-value
   contribution.
4. **Builds** — hand-made, full-concept exercises (see `builds/`).
5. **Predictions** — falsifiable rows in `predictions.md`, or scores for open
   rows with evidence.
6. **Source fixes for `pull.py`** — sites change markup; if a parse breaks, add
   or refresh a fixture in `tests/fixtures/` and update `tests/test_pull.py`.
7. **Learning-path resources** — free, project-based, verified reachable (see
   learning.md). Prove the URL with a check, don't just paste it.

## Provenance & credits (non-negotiable)

- **Every content file** (`knowledge/`, `concepts/`, `builds/`)
  carries a `Provenance:` line — `AI-drafted` or `Human-written` — and a
  `Credits:` line naming the human author(s) of its sources. AI makes mistakes;
  a reader must always be able to tell who said what.
- If you wrote the article yourself, mark `Human-written`. If an AI drafted it,
  mark `AI-drafted` and credit the human authors it summarized.
- **Credit the authors** of the articles, blog posts, and RFCs you summarize —
  name + URL + date in `## Further reading`. Do not paraphrase someone's post and let
  it stand as your own work.

## Quality rules (non-negotiable)

Every knowledge note **must** have:
- `## Further reading` with a real URL and a publish date — fetch the primary source
  before writing. Never cite a summary as the source of record.
- `Created <date> · Last verified <date>` in the header.
- `## Lesson` that transfers to a *junior backend dev*, not a generic "stay
  curious".

Every drill **must** have a pass/fail self-check the learner can run alone.

No invented URLs. No invented quotes. If you did not fetch it, you did not cite
it.

## Workflow

1. Fetch the primary source (repo, paper, official blog) — not secondary
   commentary. `python3 pull.py search "topic"` finds HN mirrors when a site is
   403-blocked.
2. Copy the template: `templates/knowledge-note.md`, `templates/concept.md`,
   or `templates/digest.md`. Drills live as a `## Drill` section inside the
   concept/knowledge note that owns them (see `templates/drill.md` for the
   section shape).
3. Write the note, then verify: `python3 -m unittest discover -s tests` still
   passes (relevant for pull.py changes) and links in your note resolve.
4. Keep the diff small. One topic, one file (its drill embedded) per PR.

## Scope

The default learner profile is a junior FastAPI/Python backend dev. Notes that
assume a different stack are welcome but must say so in the first line.
