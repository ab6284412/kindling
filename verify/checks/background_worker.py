"""Self-check for builds/background-worker.md — queue + worker + webhook.

Runs the app under a real uvicorn on port 8021 and drives it over HTTP, so the
worker's urllib POST to /webhooks/local is exercised for real (not in-process).

Usage: python3 verify/checks/background_worker.py <workdir-with-app.py>
Skips (exit 3) when Postgres is unreachable; set DATABASE_URL to point at it.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

EXIT_FAIL = 1
SKIP = 3
HOST, PORT = "127.0.0.1", 8022
BASE = f"http://{HOST}:{PORT}"


def body_json(b: bytes) -> dict:
    return json.loads(b.decode())


def http(method: str, path: str, data: bytes | None = None):
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if data is not None:
        req.add_header("content-type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=3)
        return resp.status, body_json(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, body_json(e.read())


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
    workdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("solutions", "background-worker")
    if not os.path.isfile(os.path.join(workdir, "app.py")):
        print(f"FAIL: no app.py in {workdir}")
        return EXIT_FAIL

    tmp = tempfile.mkdtemp(prefix="worker-")
    shutil.copytree(workdir, os.path.join(tmp, "work"), dirs_exist_ok=True)
    env = dict(os.environ, WEBHOOK_URL=f"{BASE}/webhooks/local")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--port", str(PORT), "--log-level", "warning"],
        cwd=os.path.join(tmp, "work"), env=env,
    )
    fails = []

    def wait_ready(timeout=15):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                status, _ = http("GET", "/todos")
                if status == 200:
                    return True
            except Exception:
                pass
            time.sleep(0.3)
        return False

    try:
        if not wait_ready():
            print("FAIL: server never became ready")
            return EXIT_FAIL

        title = f"slow-{os.getpid()}"
        t0 = time.time()
        status, d = http("POST", "/todos", json.dumps({"title": title}).encode())
        job_id = d.get("job_id")
        wall = time.time() - t0
        ok = status == 202 and bool(job_id) and wall < 1.0
        print(("PASS " if ok else "FAIL ") + f"POST returns 202 {job_id} fast ({wall:.2f}s)" + ("" if ok else f"  (status={status})"))
        if not ok:
            fails.append("202")

        status_out, jd = None, {}
        for _ in range(40):  # worker sleeps ~3s; poll up to 20s
            status_out, jd = http("GET", f"/jobs/{job_id}")
            if jd.get("status") == "done":
                break
            time.sleep(0.5)
        ok = status_out == 200 and jd.get("status") == "done"
        print(("PASS " if ok else "FAIL ") + "job transitions to done" + ("" if ok else f"  ({jd})"))
        if not ok:
            fails.append("jobdone")

        todo_id = jd.get("todo_id")
        status_out, rows = http("GET", "/webhooks")
        ok = status_out == 200 and any(r.get("todo_id") == todo_id for r in rows)
        print(("PASS " if ok else "FAIL ") + "worker POSTed a webhook delivery for the todo" + ("" if ok else f"  ({rows})"))
        if not ok:
            fails.append("webhook")

        status_out, _ = http("GET", "/todos")
        ok = status_out == 200
        print(("PASS " if ok else "FAIL ") + "API still serves while the job runs")
        if not ok:
            fails.append("alive")

        import psycopg
        db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:p@localhost:5432/postgres")
        with psycopg.connect(db_url) as conn:
            conn.execute("DELETE FROM webhooks WHERE todo_id = %s", (todo_id,))
            conn.execute("DELETE FROM jobs WHERE todo_id = %s", (todo_id,))
            conn.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            conn.commit()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n%d check(s) failed" % len(fails))
    return EXIT_FAIL if fails else 0


if __name__ == "__main__":
    sys.exit(main())
