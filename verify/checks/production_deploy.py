"""Self-check for builds/production-deploy.md — service plumbing present + alive.

Usage: python3 verify/checks/production_deploy.py <workdir>
No DB or Docker needed: checks the ops artifacts exist and the app serves
/health, /ready (503 when DB unreachable) and /metrics.
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from _asgi import request_async, run  # noqa: E402

EXIT_FAIL = 1

REQUIRED_FILES = (
    "Dockerfile",
    ".env.example",
    ".github/workflows/ci.yml",
)


def main() -> int:
    workdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("solutions", "production-deploy")
    fails = []
    for rel in REQUIRED_FILES:
        ok = os.path.isfile(os.path.join(workdir, rel))
        print(("PASS " if ok else "FAIL ") + f"artifact present: {rel}")
        if not ok:
            fails.append(rel)
    if not os.path.isfile(os.path.join(workdir, "app.py")):
        print(f"FAIL: no app.py in {workdir}")
        return EXIT_FAIL

    tmp = tempfile.mkdtemp(prefix="prod-")
    shutil.copytree(workdir, os.path.join(tmp, "work"), dirs_exist_ok=True)
    sys.path.insert(0, os.path.join(tmp, "work"))
    os.environ["DATABASE_URL"] = "postgresql://nobody:nothing@127.0.0.1:59999/nope"  # always test the degraded path
    os.environ["LOG_LEVEL"] = "ERROR"  # keep check output clean; logging is proven by the human self-check
    import app as appmod
    app = appmod.app

    async def checks():
        status, _, body = await request_async(app, "GET", "/health")
        d = json.loads(body.decode())
        ok = status == 200 and d.get("status") == "ok"
        print(("PASS " if ok else "FAIL ") + "GET /health is 200 ok")
        if not ok:
            fails.append("health")

        status, _, _ = await request_async(app, "GET", "/ready")
        ok = status == 503  # no reachable DB -> not ready
        print(("PASS " if ok else "FAIL ") + "GET /ready is 503 when DB unreachable (distinct from /health)")
        if not ok:
            fails.append("ready")

        status, _, body = await request_async(app, "GET", "/metrics")
        text = body.decode()
        ok = status == 200 and "http_requests_total" in text
        print(("PASS " if ok else "FAIL ") + "GET /metrics exposes http_requests_total")
        if not ok:
            fails.append("metrics")

    run(app, checks)
    print("\n%d check(s) failed" % len(fails))
    return EXIT_FAIL if fails else 0


if __name__ == "__main__":
    sys.exit(main())
