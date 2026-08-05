# Configuration management
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Srinively (@sriniously)

## What it is

Configuration management is how a service gets the knobs it depends on without
hard-coding them — database URLs, API keys, ports, flags, and environment
differences. Production-grade config is externalized, validated at startup, and
kept out of source control. Sriniously's ▶17 covers it.

## How it works

- **12-factor**: store config in the environment or a config store, not in code.
- **One source per value**: the app reads config once at boot into typed
  settings, not scattered `os.getenv` calls.
- **Version them like code**: default + override; dev/staging/prod differ only
  in the injected values.
- **Validate at startup**: fail fast if a required knob is missing — don't run
  half-configured and fail at request time.

## How it fails

- **Secrets committed** to git (the #1 incident class — `.env` in the repo).
- **Magic numbers in code**: a connection timeout that can only be changed by a
  redeploy.
- **Not validating at boot**: app starts with a missing DB_URL and crashes only
  on first query.
- **One giant settings blob**: unrelated values coupled so you can't vary them.
- **Config in code baked per-env**: `if stage=="prod"` branches scattered
  around instead of injected values.

## Build that proves it

[builds/production-deploy.md](../builds/production-deploy.md) — externalize DB URL + secret via
env, load into a typed settings object, and validate at startup before serving.

## Drill

Goal: prove config comes from the environment (not code) and a missing
required knob fails fast at boot — stdlib only.

Steps:
1. From a scratch dir, save this as `settings.py`:
   ```python
   import os
   DB_URL = os.getenv("DB_URL", "sqlite:///dev.db")
   PORT = int(os.getenv("PORT", "8000"))
   API_KEY = os.getenv("API_KEY")          # no default: required
   if not API_KEY:
       raise SystemExit("API_KEY not set — refusing to boot")
   print(f"booted with DB_URL={DB_URL} PORT={PORT}")
   ```
2. Run it twice, same file, different output:
   - `PORT=9000 API_KEY=x python3 settings.py`
   - `API_KEY=x python3 settings.py`
3. Prove the fail-fast: `python3 settings.py` with no `API_KEY`.

Self-check (pass/fail — run it alone):
- The first run prints `PORT=9000`, the second prints `PORT=8000` — the code
  never changed, only the environment did.
- Without `API_KEY` the process exits non-zero with the "refusing to boot"
  message *before* printing the "booted" line — it never serves half-configured.

Why this matters: 12-factor config means no code changes per environment and
no half-configured servers — every knob lives in the env/compose file, and a
missing one fails at boot, not on the first request.

## Further reading
- Sriniously, "Production-grade Configuration Management" (▶17) — https://www.youtube.com/watch?v=GR9NtirPXyc (Jul 24, 2025)
- 12-factor config — https://12factor.net/config (referenced by ▶17; fetched Aug 4 2026)