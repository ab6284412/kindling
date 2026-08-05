"""Shared stdlib ASGI test client for the build self-checks.

Exercises a FastAPI app through its real ASGI entrypoint (routing, deps,
middleware, lifespan) with no server, no httpx, no TestClient. Good enough to
prove a build spec's behavior.
"""
from __future__ import annotations

import asyncio
import json


async def request_async(app, method: str, path: str, headers=None, body: bytes = b"", query: bytes = b""):
    """One ASGI request. Returns (status:int, headers:dict[str,str], body:bytes)."""
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": query,
        "root_path": "",
        "headers": [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    status, resp_headers, chunks = None, [], []

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(msg):
        nonlocal status, resp_headers, chunks
        if msg["type"] == "http.response.start":
            status = msg["status"]
            resp_headers = msg["headers"]
        elif msg["type"] == "http.response.body":
            chunks.append(msg.get("body", b""))

    await app(scope, receive, send)
    return status, {k.decode("latin-1"): v.decode("latin-1") for k, v in resp_headers}, b"".join(chunks)


def json_post(app, path: str, payload: dict, token: str | None = None):
    headers = {"content-type": "application/json"}
    if token:
        headers["authorization"] = f"Bearer {token}"
    return request_async(
        app, "POST", path, headers=headers, body=json.dumps(payload).encode()
    )


def run(app, fn) -> None:
    """Run async fn() inside one event loop, entering the app's lifespan once."""
    async def _bootstrap():
        async with app.router.lifespan_context(app):
            await fn()

    asyncio.run(_bootstrap())
