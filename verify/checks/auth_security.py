"""Self-check for builds/auth-security.md — auth + authorization via ASGI.

Usage: python3 verify/checks/auth_security.py <workdir-with-app.py>
Runs in a temp copy of the workdir. Simulates "restart" by re-running the
startup handler (which wipes the sessions table in the reference solution).
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from _asgi import json_post, request_async, run  # noqa: E402

EXIT_FAIL = 1
JSON = {"content-type": "application/json"}


def body_json(b: bytes) -> dict:
    return json.loads(b.decode())


def main() -> int:
    workdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("solutions", "auth-security")
    src = os.path.join(workdir, "app.py")
    if not os.path.isfile(src):
        print(f"FAIL: no app.py in {workdir}")
        return EXIT_FAIL

    tmp = tempfile.mkdtemp(prefix="auth-")
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
        status, _, body = await json_post(app, "/register", {"email": "a@x.io", "password": "hunter2ok"})
        d = body_json(body)
        ok = status == 201 and "password_hash" not in body.decode() and "salt" not in body.decode() and d.get("email") == "a@x.io"
        print(("PASS " if ok else "FAIL ") + "register 201, no hash/salt leaked" + ("" if ok else f"  ({status}, {body.decode()})"))
        if not ok:
            fails.append("register")

        status, _, _ = await json_post(app, "/register", {"email": "not-an-email"})
        ok = status == 422
        print(("PASS " if ok else "FAIL ") + "invalid email is 422" + ("" if ok else f"  (got {status})"))
        if not ok:
            fails.append("bademail")

        status, _, _ = await json_post(app, "/register", {"email": "a@x.io", "password": "other"})
        ok = status == 409
        print(("PASS " if ok else "FAIL ") + "duplicate email is 409")
        if not ok:
            fails.append("dup")

        status, _, _ = await json_post(app, "/login", {"email": "a@x.io", "password": "wrong"})
        ok = status == 401
        print(("PASS " if ok else "FAIL ") + "wrong password is uniform 401")
        if not ok:
            fails.append("badlogin")

        status, _, body = await json_post(app, "/login", {"email": "a@x.io", "password": "hunter2ok"})
        d = body_json(body)
        token = d.get("token")
        ok = status == 200 and bool(token) and bool(d.get("expires_at"))
        print(("PASS " if ok else "FAIL ") + "login returns {token, expires_at}" + ("" if ok else f"  ({status}, {d})"))
        if not ok:
            fails.append("login")
        if not token:
            return

        status, _, _ = await request_async(app, "GET", "/todos")
        ok = status == 401
        print(("PASS " if ok else "FAIL ") + "unauthenticated CRUD is 401")
        if not ok:
            fails.append("unauth")

        status, _, body = await request_async(app, "GET", "/me", headers={"authorization": f"Bearer {token}"})
        d = body_json(body)
        ok = status == 200 and d.get("email") == "a@x.io"
        print(("PASS " if ok else "FAIL ") + "GET /me returns the user" + ("" if ok else f"  ({status}, {d})"))
        if not ok:
            fails.append("me")

        for email in ("b@x.io", "c@x.io"):
            await json_post(app, "/register", {"email": email, "password": "pw"})
        _, _, bbody = await json_post(app, "/login", {"email": "b@x.io", "password": "pw"})
        _, _, cbody = await json_post(app, "/login", {"email": "c@x.io", "password": "pw"})
        btok, ctok = body_json(bbody)["token"], body_json(cbody)["token"]

        status, _, body = await json_post(app, "/todos", {"title": "b owns this"}, token=btok)
        d = body_json(body)
        tid = d.get("id")
        ok = status == 201 and d.get("owner_id") == 2
        print(("PASS " if ok else "FAIL ") + "B creates a todo as owner" + ("" if ok else f"  ({status}, {d})"))
        if not ok:
            fails.append("bcreate")

        status, _, _ = await request_async(app, "GET", f"/todos/{tid}", headers={"authorization": f"Bearer {ctok}"})
        ok = status == 403
        print(("PASS " if ok else "FAIL ") + "non-owner GET is 403")
        if not ok:
            fails.append("forbid1")

        status, _, _ = await request_async(
            app, "PATCH", f"/todos/{tid}",
            headers={**JSON, "authorization": f"Bearer {ctok}"},
            body=json.dumps({"done": True}).encode(),
        )
        ok = status == 403
        print(("PASS " if ok else "FAIL ") + "non-owner PATCH is 403")
        if not ok:
            fails.append("forbid2")

        status, _, _ = await request_async(app, "DELETE", f"/todos/{tid}", headers={"authorization": f"Bearer {ctok}"})
        ok = status == 403
        print(("PASS " if ok else "FAIL ") + "non-owner DELETE is 403")
        if not ok:
            fails.append("forbid3")

        status, _, _ = await request_async(app, "GET", f"/todos/{tid}", headers={"authorization": f"Bearer {btok}"})
        ok = status == 200
        print(("PASS " if ok else "FAIL ") + "owner GET is 200")
        if not ok:
            fails.append("owner")

        # Restart proof: re-run the app's registered startup handler(s), which
        # recreate the sessions table -> old token invalid. Uses router.on_startup
        # so we don't hardcode the solution's function name.
        for handler in getattr(app.router, "on_startup", []):
            handler()
        status, _, _ = await request_async(app, "GET", "/me", headers={"authorization": f"Bearer {token}"})
        ok = status == 401
        print(("PASS " if ok else "FAIL ") + "restart wipes sessions: old token is 401 (fresh boot has no valid tokens)")
        if not ok:
            fails.append("restart")

        # Expired token: back-date the session row, then /me must 401.
        await json_post(app, "/login", {"email": "a@x.io", "password": "hunter2ok"})
        status, _, body = await json_post(app, "/login", {"email": "a@x.io", "password": "hunter2ok"})
        tok2 = body_json(body).get("token")
        if tok2:
            import sqlite3
            conn = sqlite3.connect(os.path.join(os.getcwd(), "todo.db"))
            conn.execute(
                "UPDATE sessions SET expires_at = ? WHERE token = ?",
                ("2000-01-01T00:00:00+00:00", tok2),
            )
            conn.commit()
            conn.close()
            status, _, _ = await request_async(app, "GET", "/me", headers={"authorization": f"Bearer {tok2}"})
            ok = status == 401
            print(("PASS " if ok else "FAIL ") + "expired session token is 401" + ("" if ok else f"  (got {status})"))
            if not ok:
                fails.append("expired")

    run(app, checks)
    print("\n%d check(s) failed" % len(fails))
    os.chdir(orig_cwd)
    shutil.rmtree(tmp, ignore_errors=True)
    return EXIT_FAIL if fails else 0


if __name__ == "__main__":
    sys.exit(main())
