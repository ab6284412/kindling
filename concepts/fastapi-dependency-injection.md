# Dependency injection in FastAPI
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: Sebastián Ramírez (FastAPI docs)

## What it is

Dependency injection (DI) means your code declares the things it needs to work
and a framework provides them. In FastAPI, a path operation function says
"give me a database session / a current user / a config object" and FastAPI
builds, supplies, and (with `yield`) tears down that dependency automatically.
It is FastAPI's answer to "how do I share one connection or one auth check
across many endpoints without duplicating code?"

## How it works

- **A dependency is just a function** that can take all the same parameters a
  path operation function can — think of it as a path operation function
  without the decorator. It returns anything you want.
- **`Depends()` declares it.** You pass the function *object*, not a call:
  `commons: Annotated[dict, Depends(common_parameters)]`. When a request
  arrives, FastAPI calls the dependency with the correct parameters, takes the
  result, and assigns it to the parameter in your path operation function.
- **No registration ceremony.** You don't create a class or register anything
  globally — you just reference the function in `Depends()` and FastAPI does
  the rest. With `Annotated` (FastAPI ≥ 0.95) you can store
  `CommonsDep = Annotated[dict, Depends(common_parameters)]` and reuse it, and
  type info is preserved for editors and `mypy`.
- **Sub-dependencies build a tree.** A dependency can itself take dependencies
  (e.g. `current_user` → `active_user` → `admin_user`); FastAPI solves the
  whole tree and injects the result at each step. By default a dependency
  called more than once in the same request is cached and reused
  (`use_cache=True`).
- **Testing via overrides.** `app.dependency_overrides` is a plain dict: the
  key is the original dependency, the value is the replacement. FastAPI calls
  the override instead of the original — so tests swap a real DB/HTTP call for
  a stub without touching production code. Reset with
  `app.dependency_overrides = {}`.
- **Dependencies with `yield`** run setup code before the path operation and
  cleanup after it (the canonical case: open a DB session, yield it, close
  it) — the scoped teardown path.

## How it fails (review checklist)

- **Calling the dependency instead of passing it** — `Depends(get_db())`
  instead of `Depends(get_db)` — evaluates it at import time and breaks
  injection.
- **Hidden I/O in dependencies:** a dependency that calls the network or DB in
  every request makes tests slow and stateful; that's exactly what
  `dependency_overrides` exists to replace.
- **Returning mutable shared state** from a dependency that's cached per
  request — the object leaks across requests and gets mutated.
- **Overriding the wrong function** — the key must be the exact dependency
  callable the endpoints reference, or the override silently never applies.
- **Cleanup skipped:** a `yield` dependency whose post-yield code raises or is
  never reached (e.g. an exception swallowed earlier) can leak connections.

## Build that proves it

The stage-3 CRUD service proves it — [builds/fastapi-crud.md](../builds/fastapi-crud.md),
exercising `Depends()` + an override on this workspace's stack (learning.md
stage 3). Short rep: the `## Drill` below.

## Drill

Goal: make FastAPI inject a dependency's result, then swap it for testing
without touching the endpoint.

Steps:
1. In a scratch dir, write `app.py` (run from this repo's `web/.venv`):
   ```python
   from fastapi import Depends, FastAPI

   app = FastAPI()

   def get_tier():
       return {"tier": "free"}

   @app.get("/status")
   def status(tier: dict = Depends(get_tier)):
       return tier
   ```
2. Run `uvicorn app:app` and curl `/status` — you must get
   `{"tier":"free"}`. FastAPI called `get_tier` and injected the result.
3. Now the test stub. In a second file `test_app.py`:
   ```python
   from fastapi.testclient import TestClient
   from app import app, get_tier

   def override_tier():
       return {"tier": "pro"}

   app.dependency_overrides[get_tier] = override_tier
   client = TestClient(app)

   def test_status_is_overridden():
       assert client.get("/status").json() == {"tier": "pro"}
   ```
   Run with `python -m pytest test_app.py` — from a venv with
   fastapi+httpx+pytest installed (`pip install pytest httpx` first; they are
   not in `web/.venv`) — the endpoint now returns `"pro"` with zero changes to
   the endpoint code.
4. Deliberately break it once: override with a *different* function than the
   one the endpoint references (e.g. a copy of `get_tier`) and confirm the
   override silently does nothing — this is the "wrong key" failure mode.

Self-check (pass/fail — run it alone):
- `/status` returns `{"tier":"free"}` before the override, `{"tier":"pro"}`
  after it, and the test passes.
- You can explain why the wrong-key override fails silently: the dict key must
  be the exact callable the endpoint uses.
- You can state why overrides exist (replace expensive external I/O — DB,
  HTTP, auth — in tests) rather than as a production feature.

Why this matters: testability without editing endpoints is the whole point of
DI; your real FastAPI apps (like this repo's `web/`) should be able to swap
a DB session for a fake in tests the same way.

## Further reading
- Sebastián Ramírez, https://fastapi.tiangolo.com/tutorial/dependencies/ —
  "Dependencies", FastAPI docs (fetched Aug 3 2026; Annotated form requires
  FastAPI ≥ 0.95.1)
- Sebastián Ramírez, https://fastapi.tiangolo.com/advanced/testing-dependencies/ —
  "Testing Dependencies with Overrides", FastAPI docs (fetched Aug 3 2026)
- Sebastián Ramírez, https://fastapi.tiangolo.com/reference/dependencies/ —
  `Depends()` reference (`use_cache`, `scope`; fetched Aug 3 2026)
