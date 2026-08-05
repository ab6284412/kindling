"""Self-check for builds/http-server.md — spawn server.py and probe it.

Usage: python3 verify/checks/http_server.py <workdir-with-server.py>
"""
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

EXIT_FAIL = 1
HOST, PORT = "127.0.0.1", 8000


def main() -> int:
    workdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("solutions", "http-server")
    src = os.path.join(workdir, "server.py")
    if not os.path.isfile(src):
        print(f"FAIL: no server.py in {workdir}")
        return EXIT_FAIL

    try:
        sock = socket.create_connection((HOST, PORT), timeout=1)
        sock.close()
        print(f"SKIP: port {PORT} already in use — free it or the probe hits the wrong server")
        return 3
    except OSError:
        pass

    proc = subprocess.Popen([sys.executable, src], cwd=workdir)
    base = f"http://{HOST}:{PORT}"
    fails = []

    def wait_ready(timeout=5):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                return urllib.request.urlopen(base + "/health", timeout=1).status == 200
            except Exception:
                time.sleep(0.2)
        return False

    def probe(label, method, path, data=None, expect_status=None, expect_body=None, headers=None):
        req = urllib.request.Request(base + path, data=data, method=method)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        try:
            resp = urllib.request.urlopen(req, timeout=3)
            status, body = resp.status, resp.read().decode()
        except urllib.error.HTTPError as e:
            status, body = e.code, e.read().decode()
        ok = True
        detail = f"(status={status}, body={body!r})"
        if expect_status is not None and status != expect_status:
            ok = False
        if expect_body is not None and expect_body not in body:
            ok = False
        print(("PASS " if ok else "FAIL ") + label + ("" if ok else detail))
        if not ok:
            fails.append(label)
        return status, body

    if not wait_ready():
        print("FAIL: server never became ready")
        proc.terminate()
        return EXIT_FAIL

    probe("GET / is 200 hello", "GET", "/", expect_status=200, expect_body="hello")
    probe("GET /health is 200 ok", "GET", "/health", expect_status=200, expect_body="ok")
    probe("GET /nope is 404", "GET", "/nope", expect_status=404)
    probe("POST /echo echoes body", "POST", "/echo", data=b"ping", expect_status=200, expect_body="ping")
    probe("GET /echo is 411", "GET", "/echo", expect_status=411)

    try:
        with socket.create_connection((HOST, PORT), timeout=3) as s:
            s.sendall(b"GARBAGE\r\n\r\n")
            line = s.recv(1024).decode("latin-1").split("\r\n", 1)[0]
        ok = line == "HTTP/1.1 400 Bad Request"
        print(("PASS " if ok else "FAIL ") + "garbage request line is 400" + ("" if ok else f"  (got {line!r})"))
        if not ok:
            fails.append("400")
    except OSError as e:
        print(f"FAIL: raw-socket 400 probe errored: {e}")
        fails.append("400")

    try:
        with socket.create_connection((HOST, PORT), timeout=3) as s:
            s.sendall(b"POST /echo HTTP/1.1\r\nHost: x\r\nContent-Length: 5\r\n\r\nping")
            s.shutdown(socket.SHUT_WR)
            resp = s.recv(4096).decode("latin-1")
            line = resp.split("\r\n", 1)[0]
        ok = line == "HTTP/1.1 411 Length Required"
        print(("PASS " if ok else "FAIL ") + "mismatched Content-Length is 411" + ("" if ok else f"  (got {line!r})"))
        if not ok:
            fails.append("411")
    except OSError as e:
        print(f"FAIL: raw-socket 411 probe errored: {e}")
        fails.append("411")

    proc.terminate()
    print("\n%d check(s) failed" % len(fails))
    return EXIT_FAIL if fails else 0


if __name__ == "__main__":
    sys.exit(main())
