#!/usr/bin/env python3
"""Reference solution for builds/python-from-zero.md. Stdlib only."""
import argparse
import json
import os
import sys

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")


def load() -> list[dict]:
    if not os.path.exists(STORE):
        return []
    try:
        with open(STORE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        os.replace(STORE, STORE + ".bak")
        return []


def save(todos: list[dict]) -> None:
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)


def next_id(todos: list[dict]) -> int:
    return max((t["id"] for t in todos), default=0) + 1


def cmd_add(title: str) -> int:
    todos = load()
    tid = next_id(todos)
    todos.append({"id": tid, "title": title, "done": False})
    save(todos)
    print(f"added #{tid}")
    return 0


def cmd_list() -> int:
    for t in load():
        box = "[x]" if t["done"] else "[ ]"
        print(f"{box} {t['id']} {t['title']}")
    return 0


def _find(tid: int, todos: list[dict]) -> int | None:
    for i, t in enumerate(todos):
        if t["id"] == tid:
            return i
    return None


def cmd_done(tid: int) -> int:
    todos = load()
    i = _find(tid, todos)
    if i is None:
        print(f"no todo #{tid}", file=sys.stderr)
        return 1
    todos[i]["done"] = True
    save(todos)
    print(f"done #{tid}")
    return 0


def cmd_rm(tid: int) -> int:
    todos = load()
    i = _find(tid, todos)
    if i is None:
        print(f"no todo #{tid}", file=sys.stderr)
        return 1
    todos.pop(i)
    save(todos)
    print(f"removed #{tid}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="todo.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    a = sub.add_parser("add")
    a.add_argument("title")
    for name in ("done", "rm"):
        d = sub.add_parser(name)
        d.add_argument("id", type=int)

    args = p.parse_args(argv)
    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "add":
        return cmd_add(args.title)
    if args.cmd == "done":
        return cmd_done(args.id)
    if args.cmd == "rm":
        return cmd_rm(args.id)
    return 2


if __name__ == "__main__":
    sys.exit(main())
