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

## Further reading
- Sriniously, "Production-grade Configuration Management" (▶17) — https://www.youtube.com/watch?v=GR9NtirPXyc (Jul 24, 2025)
- 12-factor config — https://12factor.net/config (referenced by ▶17; fetched Aug 4 2026)