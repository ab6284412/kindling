"""CI smoke tests for solutions/production-deploy. Stdlib + pytest + TestClient.

The app must import and serve /health even with no DATABASE_URL configured —
that's the degraded path CI can always run.
"""
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_is_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ready_degraded_without_db():
    # The test env has no DATABASE_URL -> readiness must fail closed.
    r = client.get("/ready")
    assert r.status_code == 503


def test_metrics_expose_counters():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_requests_total" in r.text


def test_request_id_header_on_error():
    r = client.get("/nope")
    assert r.status_code == 404
    assert r.headers.get("x-request-id")
