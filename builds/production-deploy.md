# Build: production, ops & scale — run it like a service
Source: [concepts/containers-docker.md](../concepts/containers-docker.md), [concepts/docker-compose.md](../concepts/docker-compose.md),
[concepts/ci-cd.md](../concepts/ci-cd.md),
[concepts/building-for-scale.md](../concepts/building-for-scale.md), and Sriniously's playlist videos ▶17
(Config management), ▶18 (Observability), ▶19 (Graceful shutdown), ▶21 (Scaling
Part-1), ▶22 (Scaling Part-2)
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

Goal: take the API from stages 3–6 and run it like a service — Docker image,
env-driven config, CI, structured logs + metrics, graceful shutdown, and a
load-test that finds and fixes one real bottleneck.

## Spec

1. **Dockerfile** — multi-stage (`python:3.12-slim` builder → slim runtime),
   runs as a non-root user, `EXPOSE 8000`, `HEALTHCHECK` hitting `/health`.
2. **12-factor config (▶17)** — every environment-dependent value via env vars
   with defaults: `DATABASE_URL`, `SECRET_KEY`, `LOG_LEVEL`. Commit a
   `.env.example` (never a real `.env`).
3. **Readiness vs liveness** — `/health` (is the process alive) and `/ready`
   (can it serve: DB reachable). Different checks on purpose.
4. **Graceful shutdown (▶19)** — a FastAPI `lifespan` that, on SIGTERM, stops
   accepting new work, drains in-flight requests, flushes, then exits cleanly
   with code 0. No `kill -9` needed.
5. **Structured logs (▶18)** — JSON-lines logging with a request id, at
   `LOG_LEVEL`; the auth build's rule holds: never log secrets.
6. **Metrics** — a minimal `/metrics` endpoint exposing stdlib-counters
   (request count, a latency histogram via `time`). No Prometheus lib in v1.
 7. **CI (GitHub Actions)** — on push: `ruff check`, `pytest`, `docker build`.
    GitHub only auto-runs workflows at the **repo root** `.github/workflows/`,
    so this repo keeps the canonical workflow at
    `solutions/production-deploy/.github/workflows/ci.yml` (verified by the
    stage-7 check) and a copy at `.github/workflows/production-deploy.yml`
    (which GitHub actually runs). Both run `ruff`, `pytest`, `docker build`
    against the solution dir. A passing run needs: ruff-clean code (add
    `# noqa` for a deliberate blind catch), at least one pytest file (empty
    suites exit 5, which is a failure), and no custom `SIGTERM` handler that
    shadows uvicorn's graceful shutdown.
8. **Load test** — `wrk`/`hey`/`ab` against the running container. Record a
   baseline (req/s, p50, p95). Find the top bottleneck (cache misses from
   stage 5, the blocking `sleep` from stage 6, an N+1 query), fix it, and
   re-measure. p95 must improve, and the fix must be explained in one line.
9. **Restart test** — `docker stop` mid-traffic: process exits within the grace
   period, no orphan connections hang.

## Constraints

- Stdlib + FastAPI + psycopg only. No orchestration (Kubernetes is an
  extension, not v1). No managed observability SaaS — the self-hosted minimal
  `/metrics` + JSON logs are enough to prove the point.
- The load-test fix must be a real change to the app (not "buy a bigger box").

## Self-check (pass/fail)

```bash
docker build -t api .          # builds green
docker run --rm -p 8000:8000 -e DATABASE_URL=... -e SECRET_KEY=dev api
curl -s localhost:8000/health   # 200 {"status":"ok"}
curl -s localhost:8000/ready    # 200 when DB reachable; 503 when not
# env override without code change:
docker run --rm -p 8000:8000 -e LOG_LEVEL=DEBUG api   # DEBUG lines appear

# graceful shutdown — fire traffic, then:
docker stop <container>         # stops within the grace period, no SIGKILL (137)

# load test — baseline vs fixed numbers recorded in the build notes:
wrk -t4 -c50 -d10s http://localhost:8000/health
# e.g. before: p95 210ms → after: p95 42ms. Explain the fix in one line.
```

## Extensions (only after v1 passes)

- Prometheus + Grafana dashboards for `/metrics`; alert on p95 (▶18).
- Compose stack (`compose.yaml`: app + Postgres + a Redis cache) replacing the
  single `docker run` — see [concepts/docker-compose.md](../concepts/docker-compose.md).
- Kubernetes/ECS deployment with rolling deploys (▶21, ▶22).
- Distributed trace ids across services.
- Autoscaling driven by p95 latency.

## Why this matters

Config, observability, graceful shutdown, and load testing are the difference
between "a project that works" and "a service someone can be paged for" — and
they're exactly what a senior reviewer or interviewer probes. The checklist is
also what makes a deployment safe to roll out at night.