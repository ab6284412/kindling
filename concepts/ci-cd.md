# CI / CD
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, GitHub Docs

## What it is

The roadmap's twelfth step: **continuous integration** (run tests and build
checks automatically on every push) and **continuous delivery/deployment**
(ship those verified changes to a target environment automatically). The
tool for this workspace: GitHub Actions.

## How it works

A pipeline is a sequence of stages triggered by a git event (`push`, PR,
tag): *checkout → install deps → lint → test → build → deploy*. Green
pipeline = safe to merge. The value is mechanical enforcement: the same
steps run on every change, and only changes that pass get in.

## How it fails (review checklist)

- **CI that tests but never deploys (or vice versa)** — the loop is closed
  only when both halves run.
- **Flaky tests breaking the pipeline** — then the team starts skipping CI,
  and it's worse than no CI. Fix the flakes.
- **Secrets in the pipeline** — Actions secrets are the right place, env
  files are not; a leaked token in logs is a breach.
- **No verification that the deployed thing is the tested thing** — build
  artifacts, don't rebuild in prod.

## Build that proves it

No build yet. This workspace's stage 5 covers it (Full Stack Open + DevOps
with Docker). The drill: a `.github/workflows/ci.yml` that runs this
workspace's unittest suite on push, then a deploy job — one of your own
APIs.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "CI / CD" step (fetched Aug 3 2026)
- GitHub Docs, https://docs.github.com/en/actions — "GitHub Actions
  documentation" (fetched Aug 3 2026)
