# Testing
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, pytest documentation

## What it is

The roadmap's eleventh step: proving your code does what you claim, in three
granularities — **unit, integration, and functional testing**. The roadmap
lists all three; for this stack the tool is pytest.

## The concepts

- **Unit tests** — test one function/class in isolation, dependencies
  faked; fast, run everywhere, catch logic errors.
- **Integration tests** — test units *together*: app + database + real
  components; catch contract mismatches (wrong SQL, bad serialization).
- **Functional tests** — test the system from the outside through the real
  interface (HTTP call, user flow); the "does the feature actually work?"
  check.

## How it works

A pyramid: many fast unit tests at the base, fewer slower integration tests,
fewest end-to-end functional tests. FastAPI gives you an in-process
`TestClient` that makes functional tests cheap — no browser needed. This
workspace's `web/tests/test_web.py` (13 tests) is a working example.

## How it fails (review checklist)

- **Testing implementation, not behavior** — a test that fails when you
  refactor without changing behavior is a liability, not a test.
- **Only unit tests, no integration** — the seams between units are where
  the bugs live; a Python-level unit test won't catch a wrong SQL query.
- **Sleep-based waiting** — flaky; wait for the actual condition.
- **Tests that pass but never ran** — the CI pipeline is the guarantee; a
  test you don't run is a rumor.

## Build that proves it

This workspace's test suite (`web/tests/`, run with `python -m unittest`)
is the model. The drill: write a unit test, an integration test against a
real database, and a functional test through FastAPI's TestClient for one
endpoint.

## Drill

Goal: pin a failure path with FastAPI's TestClient and prove a test encodes
the endpoint's contract. Depends on FastAPI + httpx (already installed);
unittest is stdlib.

Steps:
1. Save this as `test_api_drill.py`:
   ```python
   from fastapi import FastAPI
   from fastapi.responses import JSONResponse
   from fastapi.testclient import TestClient
   import unittest

   app = FastAPI()

   @app.get("/divide")
   def divide(a: int, b: int):
       return a / b            # b=0 -> uncaught ZeroDivisionError -> 500

   @app.get("/items/{item_id}")
   def get_item(item_id: int):
       if item_id not in {1, 2}:
           return JSONResponse(status_code=404, content={"error": "not found"})
       return {"id": item_id}

   class TestAPI(unittest.TestCase):
       def setUp(self):
           self.c = TestClient(app, raise_server_exceptions=False)

       def test_divide_by_zero_is_500(self):
           self.assertEqual(self.c.get("/divide?a=1&b=0").status_code, 500)

       def test_missing_item_is_404(self):
           self.assertEqual(self.c.get("/items/99").status_code, 404)

   if __name__ == "__main__":
       unittest.main()
   ```
2. Run `python3 test_api_drill.py -v` — both tests pass (the 500 documents a
   real bug, not a feature).
3. Fix the endpoint: wrap `a / b` in `try/except ZeroDivisionError` and
   `return JSONResponse(status_code=400, content={"error": "division by
   zero"})` (a bare `return 400` would serialize as a *200* body — the status
   code is the contract, so set it explicitly), then re-run the suite.

Self-check (pass/fail — run it alone): the suite is green on the first run —
but the green `test_divide_by_zero_is_500` means "we leak a raw exception as a
500", a real bug, not a feature. Now do step 3's fix (catch the error, return
`400`) and re-run: `test_divide_by_zero_is_500` FAILS until you update it to
expect `400`, and only then is the suite green again. If you changed the
endpoint's behavior and no test changed color, your test is asserting the
wrong thing.

Why this matters: a green test that pins a bug is a trap — the status code is
the contract, and the test suite is what keeps a broken response from
shipping.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Testing" step (fetched Aug 3 2026)
- pytest documentation, https://docs.pytest.org/en/stable/ (fetched Aug 3 2026)
