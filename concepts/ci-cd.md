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

Proven by [builds/production-deploy.md](../builds/production-deploy.md) — its CI job
(`solutions/production-deploy/.github/workflows/ci.yml`) runs this workspace's
unittest suite on push. This workspace's stage 7 covers it (Full Stack Open +
DevOps with Docker).

## Drill

Goal: prove a CI pipeline gates merging — a red change fails and stops, a
green one reaches "deploy" — by running a fake pipeline locally (stdlib).

Steps:
1. From a scratch dir, create a tiny app and test:
   `app.py`:
   ```python
   def add(a, b): return a + b
   ```
   `test_app.py`:
   ```python
   import unittest, app
   class T(unittest.TestCase):
       def test_add(self): self.assertEqual(app.add(1, 2), 3)
   if __name__ == "__main__": unittest.main()
   ```
2. Save this fake CI as `ci.py` and run `python3 ci.py`:
   ```python
   import subprocess, sys
   stages = [
       ("lint", ["python3", "-m", "py_compile", "app.py"]),
       ("test", ["python3", "-m", "unittest", "test_app.py"]),
   ]
   for name, cmd in stages:
       r = subprocess.run(cmd, capture_output=True, text=True)
       print(f"[{name}] {'PASS' if r.returncode == 0 else 'FAIL'}")
       if r.returncode != 0:
           print(r.stdout, r.stderr)
           sys.exit(1)            # pipeline stops — nothing deploys
   print("[deploy] shipping...")
   ```
3. Break the app (change `add` to `return a - b`), rerun.

Self-check (pass/fail — run it alone):
- Green run prints `[lint] PASS`, `[test] PASS`, then `[deploy] shipping...`
  and `echo $?` prints 0.
- Red run prints `[test] FAIL` and the traceback, never prints `[deploy]`,
  and exits non-zero — a broken change is mechanically blocked before it
  ships.

Why this matters: CI's value is enforcement, not convenience — the same
stages run on every push and only green code gets in; skipping or ignoring
a red pipeline is how bad changes reach prod.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "CI / CD" step (fetched Aug 3 2026)
- GitHub Docs, https://docs.github.com/en/actions — "GitHub Actions
  documentation" (fetched Aug 3 2026)
