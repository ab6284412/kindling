"""Self-check for builds/storage-cache.md — Postgres + cache coherence via ASGI.

Usage: python3 verify/checks/storage_cache.py <workdir-with-app.py>
Skips (exit 3) when Postgres is unreachable; set DATABASE_URL to point at it.
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from _asgi import json_post, request_async, run  # noqa: E402

EXIT_FAIL = 1
SKIP = 3
JSON = {"content-type": "application/json"}


def body_json(b: bytes) -> dict:
    return json.loads(b.decode())


def pg_reachable() -> bool:
    try:
        import psycopg
        url = os.environ.get("DATABASE_URL", "postgresql://postgres:p@localhost:5432/postgres")
        with psycopg.connect(url, connect_timeout=2):
            return True
    except Exception as e:
        print(f"SKIP: Postgres unreachable ({e}). Start it: docker run --rm "
              f"-e POSTGRES_PASSWORD=p -p 5432:5432 postgres:17-alpine, then set DATABASE_URL.")
        return False


def main() -> int:
    if not pg_reachable():
        return SKIP
    workdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("solutions", "storage-cache")
    if not os.path.isfile(os.path.join(workdir, "app.py")):
        print(f"FAIL: no app.py in {workdir}")
        return EXIT_FAIL

    tmp = tempfile.mkdtemp(prefix="storage-")
    shutil.copytree(workdir, os.path.join(tmp, "work"), dirs_exist_ok=True)
    sys.path.insert(0, os.path.join(tmp, "work"))
    import app as appmod
    app = appmod.app
    fails = []
    title = f"first-{os.getpid()}"

    async def checks():
        status, _, body = await json_post(app, "/todos", {"title": title})
        tid = body_json(body).get("id")
        ok = status == 201 and tid
        print(("PASS " if ok else "FAIL ") + "POST creates a todo" + ("" if ok else f"  ({status})"))
        if not ok:
            fails.append("post")

        status1, _, b1 = await request_async(app, "GET", f"/todos/{tid}")
        status2, _, b2 = await request_async(app, "GET", f"/todos/{tid}")
        ok = status1 == 200 and b1 == b2
        print(("PASS " if ok else "FAIL ") + "GET twice returns identical content (miss then hit)")
        if not ok:
            fails.append("cache")

        status, _, body = await request_async(
            app, "PATCH", f"/todos/{tid}",
            headers=JSON, body=json.dumps({"done": True}).encode(),
        )
        ok = status == 200 and body_json(body).get("done") is True
        print(("PASS " if ok else "FAIL ") + "PATCH updates the row" + ("" if ok else f"  ({status})"))
        if not ok:
            fails.append("patch")

        status, _, body = await request_async(app, "GET", f"/todos/{tid}")
        ok = status == 200 and body_json(body).get("done") is True
        print(("PASS " if ok else "FAIL ") + "PATCH invalidated the cache (fresh read sees the change)")
        if not ok:
            fails.append("invalidate")

        # Cache-presence proof: a cacheless solution passes everything above, so
        # flip the row out-of-band — a cached read must return the STALE value.
        import psycopg
        with psycopg.connect(appmod.DATABASE_URL) as conn:
            conn.execute("UPDATE todos SET done = NOT done WHERE id = %s", (tid,))
            conn.commit()
        status, _, body = await request_async(app, "GET", f"/todos/{tid}")
        ok = status == 200 and body_json(body).get("done") is True
        print(("PASS " if ok else "FAIL ") + "out-of-band write is not seen (a real cache serves stale data)" + ("" if ok else f"  ({status}, {body})"))
        if not ok:
            fails.append("cache-presence")
        with psycopg.connect(appmod.DATABASE_URL) as conn:
            conn.execute("UPDATE todos SET done = NOT done WHERE id = %s", (tid,))
            conn.commit()

        status, _, _ = await json_post(app, "/todos", {"title": title})
        ok = status == 409
        print(("PASS " if ok else "FAIL ") + "duplicate unique title is 409")
        if not ok:
            fails.append("unique")

        with psycopg.connect(appmod.DATABASE_URL) as conn:
            audits = conn.execute(
                "SELECT COUNT(*) AS n FROM audit_log WHERE todo_id = %s", (tid,)
            ).fetchone()[0]
        ok = audits == 1
        print(("PASS " if ok else "FAIL ") + "create wrote exactly one audit row (transaction)" + ("" if ok else f"  (got {audits})"))
        if not ok:
            fails.append("audit")

        status, _, _ = await request_async(app, "DELETE", f"/todos/{tid}")
        ok = status == 204
        print(("PASS " if ok else "FAIL ") + "DELETE returns 204")
        if not ok:
            fails.append("del")

        status, _, _ = await request_async(app, "GET", f"/todos/{tid}")
        ok = status == 404
        print(("PASS " if ok else "FAIL ") + "DELETE evicted the cache (404 after delete)")
        if not ok:
            fails.append("evict")

        with psycopg.connect(appmod.DATABASE_URL) as conn:
            orphans = conn.execute(
                "SELECT COUNT(*) AS n FROM audit_log WHERE todo_id = %s", (tid,)
            ).fetchone()[0]
        ok = orphans == 0
        print(("PASS " if ok else "FAIL ") + "delete cascaded the audit rows (no orphans)" + ("" if ok else f"  (got {orphans})"))
        if not ok:
            fails.append("cascade")

    run(app, checks)
    print("\n%d check(s) failed" % len(fails))
    import psycopg
    with psycopg.connect(appmod.DATABASE_URL) as conn:
        conn.execute("DELETE FROM todos WHERE title LIKE 'first-%'")  # cascades audit rows
        conn.commit()
    shutil.rmtree(tmp, ignore_errors=True)
    return EXIT_FAIL if fails else 0


if __name__ == "__main__":
    sys.exit(main())
