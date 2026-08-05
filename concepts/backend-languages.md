# Pick a Backend Language
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Python Software Foundation

## What it is

The roadmap's second step: choose one backend language and learn it deeply.
The roadmap lists Python, JavaScript (Node), Go, Rust, Java, PHP, C#, and
Ruby, with **Python** and **Go** marked as personal recommendations and the
rest as "pick this or purple" alternatives. For this workspace the choice is
Python.

## The concepts

- **Python** — dynamically typed, beginner-friendly, huge ecosystem;
  FastAPI/Django/Flask. Recommended by the roadmap.
- **JavaScript (Node)** — the only language that's both frontend and backend;
  event loop + npm.
- **Go** — statically typed, compiled, trivial concurrency (goroutines);
  the modern pick for infra/APIs.
- **Rust** — memory-safe systems language; used where Node/Go aren't fast
  enough.
- **Java** — long-running enterprise workhorse (Spring).
- **PHP** — server-rendered web (Laravel); huge legacy surface.
- **C#** — Microsoft's Java counterpart (.NET).
- **Ruby** — developer-experience-first (Rails).

## How it fails (review checklist)

- **Language-hopping:** learning 4 languages shallowly beats 1 deeply for
  hiring; the roadmap's whole point is depth in one.
- **Confusing ecosystem with language:** "learning Python" is really
  learning the stdlib + packaging + one framework. This workspace's stage 1
  (`learning.md`) covers Python foundations.

## Build that proves it

This workspace's stage 1 project: freeCodeCamp "Python Certification (v9)"
cert. Finish it before reading the rest of the roadmap's topics.

## Drill

Goal: feel the static-vs-dynamic typing difference by running one tiny program
in Python and in Go.

Steps:
1. Dependency: Go installed (`go version`). In a scratch dir, write `sum.py`
   and `sum.go`, each computing `sum(range(10))` (0+…+9) and printing it.
2. Run `python3 sum.py` and `go run sum.go` — both must print `45`.
3. Break the type in each: change the accumulator to a string (`total = "x"`
   in Python, `var total string` in Go) and re-run. Go's `go run` refuses to
   compile; Python only errors when the string hits the arithmetic — after the
   program already started.

Self-check (pass/fail):
- Both programs print `45` in step 2.
- Step 3: Go fails at compile time (a `go run` error), Python at runtime —
   you can state which failure happened *before* the program ran and which
   during.
- You can say which of these the roadmap recommends and which one this
   workspace chose (and why).

Why this matters: "pick one language and learn it deeply" only sticks if you
can feel what your language's type system checks before a request ever reaches
your code.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Pick a Backend Language" step
  (fetched Aug 3 2026)
- Python Software Foundation, https://www.python.org/ (fetched Aug 3 2026)
