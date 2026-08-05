"""Self-check for builds/python-from-zero.md. Runs todo.py in a scratch dir.

Usage: python3 verify/checks/python_foundation.py <workdir-with-todo.py>
"""
import os
import shutil
import subprocess
import sys
import tempfile

EXIT_FAIL = 1
SKIP = 3


def run(cmd, cwd) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> int:
    workdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("solutions", "python-foundation")
    src = os.path.join(workdir, "todo.py")
    if not os.path.isfile(src):
        print(f"FAIL: no todo.py in {workdir}")
        return EXIT_FAIL

    tmp = tempfile.mkdtemp(prefix="pyfound-")
    shutil.copy(src, os.path.join(tmp, "todo.py"))
    py = sys.executable
    fails = []

    def expect(label, cmd, want_rc, want_out=None, want_missing=None):
        rc, out = run(cmd, tmp)
        ok = rc == want_rc
        if ok and want_out is not None:
            ok = want_out in out
        if ok and want_missing is not None:
            ok = want_missing not in out
        print(("PASS " if ok else "FAIL ") + label + ("" if ok else f"  (rc={rc}, out={out!r})"))
        if not ok:
            fails.append(label)

    rc, out = run([py, "-c", "import todo"], tmp)
    ok = rc == 0
    print(("PASS " if ok else "FAIL ") + "imports without side effects (no crash, no output)" + ("" if ok else f"  ({out!r})"))
    if not ok:
        fails.append("import-safety")

    expect("list on empty file exits 0, prints nothing",
           [py, "todo.py", "list"], 0, want_out="", )
    expect("add first task", [py, "todo.py", "add", "first task"], 0, "#1")
    expect("add second", [py, "todo.py", "add", "second"], 0, "#2")
    expect("add with no title exits 2", [py, "todo.py", "add"], 2)
    rc, out = run([py, "todo.py", "list"], tmp)
    lines = [ln for ln in out.splitlines() if ln.strip()]
    parts = [ln.split() for ln in lines]
    ids = [int(p[2]) for p in parts if len(p) >= 3 and p[2].isdigit()]
    ok = ids == sorted(ids) and len(ids) == 2 and lines and lines[0].startswith("[ ]")
    print(("PASS " if ok else "FAIL ") + "list shows both pending, strictly in id order" + ("" if ok else f"  (ids={ids})"))
    if not ok:
        fails.append("list order")
    expect("done 1", [py, "todo.py", "done", "1"], 0, "done #1")
    rc, out = run([py, "todo.py", "list"], tmp)
    ok = "[x] 1 first task" in out and "[ ] 2 second" in out
    print(("PASS " if ok else "FAIL ") + "list shows done checkbox" + ("" if ok else f"  ({out!r})"))
    if not ok:
        fails.append("checkbox")
    expect("rm 2", [py, "todo.py", "rm", "2"], 0, "removed #2")
    expect("done unknown id exits 1", [py, "todo.py", "done", "99"], 1, "no todo #99")
    expect("rm unknown id exits 1", [py, "todo.py", "rm", "99"], 1, "no todo #99")
    with open(os.path.join(tmp, "todos.json"), "w") as f:
        f.write("{broken")
    rc, out = run([py, "todo.py", "list"], tmp)
    ok = rc == 0 and os.path.exists(os.path.join(tmp, "todos.json.bak"))
    print(("PASS " if ok else "FAIL ") + "corrupt file backed up, no crash")
    if not ok:
        fails.append("corrupt")
    expect("restart adds fresh id", [py, "todo.py", "add", "third"], 0, "#1")
    rc, out = run([py, "todo.py", "list"], tmp)
    ok = "[ ] 1 third" in out and "first task" not in out
    print(("PASS " if ok else "FAIL ") + "fresh store after corruption" + ("" if ok else f"  ({out!r})"))
    if not ok:
        fails.append("fresh")

    print("\n%d check(s) failed" % len(fails))
    shutil.rmtree(tmp, ignore_errors=True)
    return EXIT_FAIL if fails else 0


if __name__ == "__main__":
    sys.exit(main())
