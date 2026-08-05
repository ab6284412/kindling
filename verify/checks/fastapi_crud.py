"""Self-check for builds/fastapi-crud.md — exercise a FastAPI CRUD app via ASGI.

Usage: python3 verify/checks/fastapi_crud.py <workdir-with-app.py>
Runs in a temp copy of the workdir so no todo.db is left behind.
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from _asgi import json_post, request_async, run  # noqa: E402

EXIT_FAIL = 1


def body_json(b: bytes) -> dict:
    return json.loads(b.decode())


def main() -> int:
    workdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("solutions", "fastapi-crud")
    src = os.path.join(workdir, "app.py")
    if not os.path.isfile(src):
        print(f"FAIL: no app.py in {workdir}")
        return EXIT_FAIL

    tmp = tempfile.mkdtemp(prefix="crud-")
    shutil.copytree(workdir, os.path.join(tmp, "work"), dirs_exist_ok=True)
    for f in os.listdir(os.path.join(tmp, "work")):
        if f.endswith(".db"):
            os.remove(os.path.join(tmp, "work", f))
    orig_cwd = os.getcwd()
    os.chdir(os.path.join(tmp, "work"))  # app uses a relative DB path
    sys.path.insert(0, os.path.join(tmp, "work"))
    import app as appmod
    app = appmod.app

    fails = []

    async def checks():
        # sqlite stores booleans as 1/0 (the build spec calls this out) — assert
        # the integer encoding, not Python True/False.
        status, _, body = await json_post(app, "/todos", {"title": "write build", "done": True})
        d = body_json(body)
        ok = status == 201 and d.get("done") == 1
        print(("PASS " if ok else "FAIL ") + "POST creates todo (201, done=1)" + ("" if ok else f"  ({status}, {d})"))
        if not ok:
            fails.append("post1")

        status, _, body = await json_post(app, "/todos", {"title": "verify it"})
        d = body_json(body)
        ok = status == 201 and d.get("done") == 0 and d.get("id") == 2
        print(("PASS " if ok else "FAIL ") + "POST defaults done=0, id=2" + ("" if ok else f"  ({status}, {d})"))
        if not ok:
            fails.append("post2")

        status, _, body = await request_async(app, "GET", "/todos")
        d = body_json(body)
        ok = status == 200 and [t["id"] for t in d] == [1, 2]
        print(("PASS " if ok else "FAIL ") + "GET /todos lists both, in order" + ("" if ok else f"  ({d})"))
        if not ok:
            fails.append("list")

        status, _, body = await request_async(app, "GET", "/todos/1")
        d = body_json(body)
        ok = status == 200 and d.get("title") == "write build"
        print(("PASS " if ok else "FAIL ") + "GET /todos/1 returns row" + ("" if ok else f"  ({status}, {d})"))
        if not ok:
            fails.append("get1")

        status, _, _ = await request_async(app, "GET", "/todos/99")
        ok = status == 404
        print(("PASS " if ok else "FAIL ") + "GET /todos/99 is 404")
        if not ok:
            fails.append("get404")

        status, _, body = await request_async(
            app, "PATCH", "/todos/2",
            headers={"content-type": "application/json"},
            body=json.dumps({"done": True}).encode(),
        )
        d = body_json(body)
        ok = status == 200 and d.get("done") == 1 and d.get("title") == "verify it"
        print(("PASS " if ok else "FAIL ") + "PATCH updates only present field" + ("" if ok else f"  ({status}, {d})"))
        if not ok:
            fails.append("patch")

        status, _, _ = await request_async(app, "DELETE", "/todos/1")
        ok = status == 204
        print(("PASS " if ok else "FAIL ") + "DELETE returns 204")
        if not ok:
            fails.append("delete")

        status, _, body = await request_async(app, "GET", "/todos")
        d = body_json(body)
        ok = status == 200 and [t["id"] for t in d] == [2]
        print(("PASS " if ok else "FAIL ") + "DELETE removed the row" + ("" if ok else f"  ({d})"))
        if not ok:
            fails.append("list2")

    run(app, checks)
    print("\n%d check(s) failed" % len(fails))
    os.chdir(orig_cwd)
    shutil.rmtree(tmp, ignore_errors=True)
    return EXIT_FAIL if fails else 0


if __name__ == "__main__":
    sys.exit(main())
