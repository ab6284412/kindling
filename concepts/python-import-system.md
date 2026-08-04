# The Python import system
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: Python Software Foundation (Python Language Reference)

## What it is

`import` is how one module gets access to another's code — the plumbing behind
`from . import render, state` in `web/app.py`. Every import is two operations:
**search** for the named module, then **bind** the result to a name in the
local scope. Understanding it is what turns "it worked on my machine" import
errors into something you can reason about.

## How it works

- **The cache first.** Search starts in `sys.modules`. If the module was
  already imported, you get it back instantly — an import is *not* re-executed
  on a second import. Deleting a key makes Python search anew next time.
- **The meta path.** If not cached, finders on `sys.meta_path` are asked in
  order: built-ins, frozen modules, then the path-based finder, which walks
  `sys.path` (directories, zip files). The first finder that returns a spec
  wins; none matching → `ModuleNotFoundError`.
- **Packages are modules with a `__path__`.** A *regular package* is a
  directory with an `__init__.py`, which is executed when the package is
  imported. A subdirectory without `__init__.py` becomes a namespace package
  (PEP 420) — a composite of portions, no single file.
- **Relative imports use dots.** One leading dot = current package, two =
  parent: `from .foo import bar`, `from ..sub import x`. Absolute imports
  (`import spam.eggs`) and relative (`from .module import x`) both exist, but
  relative imports only work inside a package, never in `__main__`.
- **`__main__` is special.** Run `python script.py` and `__main__.__spec__`
  is `None` — there is no surrounding package, so relative imports fail. Run
  with `python -m package.module` and the spec is set correctly.
- **Circular imports partially work.** The module is inserted into
  `sys.modules` *before* its code runs, so a module importing itself back does
  not recurse infinitely — but it may see a half-initialized module.

## How it fails (review checklist)

- `ModuleNotFoundError` at the top of your app: the module isn't on
  `sys.path`, the venv isn't activated, or a package dir lacks `__init__.py`.
- **Name shadowing:** a file you name `request.py` or `test.py` hides the
  stdlib/third-party module of the same name — imports suddenly resolve to
  your own code.
- **Relative import outside a package:** `ImportError: attempted relative
  import with no known parent package` when you run a file directly instead of
  with `-m`.
- **Circular imports** surface as `ImportError: cannot import name X` — a
  name that wasn't bound yet when the other module looked it up.
- **Stale assumptions about caching:** two modules can hold two *different*
  objects for the same name if one keeps a reference after a `sys.modules`
  invalidation.

## Build that proves it

No build yet (this pass is concepts + drills). Short rep: the `## Drill`
below.

## Drill

Goal: prove you can predict why an import resolves — or fails — by hand.

Steps:
1. Create a package in a scratch directory:
   ```
   lab/
     __init__.py
     app.py
     helpers/
       __init__.py
       util.py
   ```
   In `helpers/util.py` define `def ping(): return "pong"`. In `app.py`, add
   `from .helpers.util import ping` and `print(ping())`.
2. Run it correctly: `python3 -m lab.app` from the directory *above* `lab/`.
   Confirm it prints `pong`.
3. Now run the same file as a script: `python3 lab/app.py`. Observe the
   error. Explain why the relative import fails here.
4. Add a file `sys.py` (a fake stdlib module) at the top of `lab/`, then from
   `lab/app.py` run `import sys; print(sys.path)` — wait, first reproduce the
   shadowing: put `import sys` before the relative import and run with
   `python3 -m lab.app`. Observe the failure, then rename the file and
   re-run.

Self-check (pass/fail — run it alone):
- `python3 -m lab.app` prints `pong`.
- You can state, without running, which of the two runs above raises
  `ImportError: attempted relative import with no known parent package` and
  why (`__main__` has no `__spec__` when run as a script).
- You can explain the exact search order for `import sys` (cache →
  built-ins → path-based finder over `sys.path`) and name the failure mode the
  fake `sys.py` triggers.

Why this matters: "import broken" is a daily junior-backend error; the fix is
usually not Googling the error but naming which of the three lookup layers
(cache, path, shadowing) went wrong.

## Further reading
- Python Software Foundation, https://docs.python.org/3/reference/import.html —
  "5. The import system", Python Language Reference, 3.14.6 (fetched Aug 3 2026)
- Python Software Foundation, https://peps.python.org/pep-0420/ — PEP 420,
  namespace packages (Python 3.3+, 2012)
