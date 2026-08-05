# Build: Python from zero — a CLI program that persists
Source: [concepts/python-import-system.md](../concepts/python-import-system.md), [concepts/learn-the-basics-projects.md](../concepts/learn-the-basics-projects.md),
and the freeCodeCamp Python Certification (v9) that stage 1 delegates to.
Provenance: AI-drafted · Credits: freeCodeCamp, Python Software Foundation

Goal: write a complete, runnable Python program with zero third-party imports —
CLI parsing, functions, file persistence, error handling, and a pass/fail test
— proving stage 1's "write, run, and debug Python without looking it up".

## Spec

Write `todo.py` (stdlib only) that:

1. Parses subcommands with `argparse`: `add <title>`, `list`, `done <id>`,
   `rm <id>`.
2. Persists todos to `todos.json` next to the script (create it on first
   write). Each todo is `{"id": int, "title": str, "done": bool}`. A fresh
   `list` on an empty/missing file prints nothing and exits `0`.
3. `add <title>` assigns the next id (`max(existing ids) + 1`), writes the row,
   prints `added #<id>`.
4. `list` prints one line per todo: `[x] <id> <title>` when done, `[ ] <id>
   <title>` when not, in id order.
5. `done <id>` marks that id done and prints `done #<id>`; `rm <id>` deletes it
   and prints `removed #<id>`. A missing id prints `no todo #<id>` and exits
   with code `1`.
6. `add` with no title prints a usage error and exits `2`.
7. Handles a corrupted `todos.json` (not valid JSON) by backing it up to
   `todos.json.bak` and starting fresh — it must not crash.

## Constraints

- Stdlib only: `argparse`, `json`, `os`. No third-party packages.
- The program must be import-safe: `if __name__ == "__main__":` guards the CLI
  entry so `import todo` doesn't run anything.
- Data lives in the file, not memory — restarting proves persistence.

## Self-check (pass/fail)

Automated: from the repo root, `python3 verify.py build python-foundation` asserts
all of the below in one pass. To run the same checks by hand, from a scratch dir
(delete `todos.json` first), run in order:

```bash
python3 todo.py list; echo "exit=$?"            # nothing, exit=0
python3 todo.py add "first task"                # added #1
python3 todo.py add "second"                    # added #2
python3 todo.py add                              # usage error, exit=2
python3 todo.py list                             # [ ] 1 first task / [ ] 2 second
python3 todo.py done 1                           # done #1
python3 todo.py list                             # [x] 1 first task / [ ] 2 second
python3 todo.py rm 2                             # removed #2
python3 todo.py list                             # [x] 1 first task
python3 todo.py done 99                          # no todo #99, exit=1
echo '{broken' > todos.json && python3 todo.py list   # prints nothing, exit=0 (backup made)
python3 todo.py add "third"                     # added #1 (ids restart fresh)
```

- Ids must never repeat across runs; after the corruption step the ids restart
  at `1` because the file was replaced.
- Run the sequence twice, each time from a fresh scratch dir (delete
  `todos.json` before the first command) — the outputs must be identical.
  Ids are NOT stable across non-deleted runs: `add` continues from the last id,
  so a second run without a clean dir shows `#3`, `#4`, … not `#1`, `#2`. That
  is correct behavior, not a bug.

## Extensions (only after the base passes)

- `--file <path>` flag so the store isn't hardcoded next to the script.
- A `checklist` of your own dev tools: run the script under `python3 -m pdb` and
  single-step one command.
- A tiny `test_todo.py` using `unittest` that runs the command sequence in a
  temp dir and asserts the outputs.

## Why this matters

This is the smallest thing that exercises the full stage-1 loop — write, run,
debug, persist, test — with no framework in the way. Every later build assumes
you can do all of it without looking it up.
