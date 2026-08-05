#!/usr/bin/env python3
"""Reference solution for builds/http-server.md — stdlib socket HTTP/1.1 server."""
import socket

HOST, PORT = "127.0.0.1", 8000


def _response(status_line: str, body: bytes, content_type: str = "text/plain") -> bytes:
    head = f"HTTP/1.1 {status_line}\r\nContent-Type: {content_type}\r\n".encode()
    head += f"Content-Length: {len(body)}\r\n\r\n".encode()
    return head + body


def handle(conn: socket.socket) -> None:
    try:
        data = conn.recv(65536)
    except OSError:
        return
    if not data:
        return
    try:
        request_line, _, rest = data.partition(b"\r\n")
        method, target, version = request_line.decode("latin-1").split(" ", 2)
        if not version.startswith("HTTP/1"):
            raise ValueError("bad version")
    except ValueError:
        conn.sendall(_response("400 Bad Request", b"bad request"))
        return

    headers = {}
    for line in rest.split(b"\r\n"):
        if not line:
            break
        name, _, value = line.decode("latin-1").partition(":")
        headers[name.strip().lower()] = value.strip()

    if method == "GET" and target == "/":
        conn.sendall(_response("200 OK", b"hello"))
    elif method == "GET" and target == "/health":
        conn.sendall(_response("200 OK", b"ok"))
    elif target == "/echo":
        # The self-check demands GET /echo -> 411 too, so the route keys on
        # Content-Length, not on method: a body-bearing request is echoed, a
        # length-less one is 411.
        length = headers.get("content-length")
        if length is None or not length.isdigit():
            conn.sendall(_response("411 Length Required", b"length required"))
            return
        body = data.partition(b"\r\n\r\n")[2]
        while len(body) < int(length):
            more = conn.recv(int(length) - len(body))
            if not more:
                break
            body += more
        if len(body) < int(length):
            conn.sendall(_response("411 Length Required", b"length required"))
            return
        conn.sendall(_response("200 OK", body[: int(length)]))
    else:
        conn.sendall(_response("404 Not Found", b"not found"))


def serve() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        while True:
            conn, _ = srv.accept()
            with conn:
                handle(conn)  # Connection: close — one request per connection


if __name__ == "__main__":
    serve()
