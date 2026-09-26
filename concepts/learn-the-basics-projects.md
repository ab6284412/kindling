# Learn the basics (beginner projects)
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh

## What it is

The roadmap's "Learn the Basics" step — the point where the roadmap stops
listing topics and says: **build beginner and intermediate projects until
you can get a job**. It carries the roadmap's "API Styles" note (learn one
language, build lots of projects) and "Server Side" / "Containerization" /
"Container Orchestration" grouping labels (see `web-servers.md` and
`containers-docker.md`).

## The concepts

- **Beginner Project Ideas** — small, complete things: a notes API, a
  to-do CRUD, a URL shortener. Each one applies the earlier steps end-to-end
  (language → git → DB → API → tests).
- **Intermediate Project Ideas** — bigger: an auth'd multi-user service
  with a queue, caching, and deployment.
- **The meta-lesson** — "you may never need most of these [topics]; just
  know what they are and when to use them." Depth on the fundamentals,
  breadth on the catalogue.
- **How LLMs work / AI vs traditional coding / embeddings / vectors** — the
  AI-fundamentals the roadmap files under this step; covered in
  `ai-assisted-coding.md` (how LLMs work, AI vs traditional coding) and
  `ai-integration-patterns.md` (embeddings, vectors).

## How it fails (review checklist)

- **Infinite tutorials, zero projects** — watching courses is not learning;
  the roadmap's own FAQ says build projects to solidify concepts.
- **Over-scoping** — a project you finish is worth ten you architect on
  paper; this workspace's `builds/` convention exists for exactly this.

## Build that proves it

This IS the build step: complete `builds/http-server.md` and the workspace's
stage projects in `learning.md` — a finished CRUD API beats a ninth
screenshot of someone else's.

## Drill

Goal: audit which of the roadmap's earlier steps this workspace's learning.md
already turns into projects.

Steps:
1. Open `learning.md` (this repo) and read its 7 stages (Python foundation →
   request/response → API design → auth → storage → async → production).
2. Open `concepts/README.md` (the stage index) and `learning.md`'s "Walk the
   path" section.
3. For each of the first 4 roadmap steps (Introduction, Pick a Language,
   Version Control, Repo Hosting), write one line: which learning.md stage or
   `builds/*.md` build covers it, or "uncovered".
4. In one sentence each, map learning.md's stage projects to roadmap project
   ideas: notes API → to-do CRUD → URL shortener → auth'd multi-user service.

Self-check (pass/fail):
- Every one of the 4 roadmap steps has a verdict line ("covered by stage N /
  builds/X.md" or "uncovered") — no blanks.
- You can name exactly which learning.md stage is the next one you have not
  finished, and the build that proves it.
- You can name one roadmap project idea with no matching learning.md stage —
  the gap is real; that is breadth, not depth.

Why this matters: the roadmap's whole "Learn the Basics" point is finishing
projects; the audit tells you which stage to attack next instead of collecting
tutorials.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Learn the Basics" step and
  project-ideas track (fetched Aug 3 2026)
