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

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Testing" step (fetched Aug 3 2026)
- pytest documentation, https://docs.pytest.org/en/stable/ (fetched Aug 3 2026)
