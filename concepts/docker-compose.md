# Docker Compose
Created 2026-08-06 · Last verified 2026-08-06
Provenance: AI-drafted · Credits: Docker Docs (Compose)

## What it is

Compose is the tool for defining and running **multi-container** applications:
one YAML file declares every service, network, and volume, and one command
starts them all. Where `containers-docker.md`'s `Dockerfile` packages *one*
service, Compose assembles the *stack* — the FastAPI app + Postgres + Redis +
worker that a real backend is. It is the standard way a junior FastAPI dev
runs a full local environment.

## How it works

The application model has three named pieces (from the Compose Spec docs):

- **Services** — the containers: each is "the same container image, and
  configuration, one or more times". A service is `image:` or `build:`, plus
  `ports:`, `environment:`, `volumes:`, `depends_on:`, healthchecks.
- **Networks** — the IP routes between services; containers on one network can
  reach each other by service name, which is your `DATABASE_URL` host without
  an IP.
- **Volumes** — the persistent data that survives container restarts; declared
  at the top level and mounted into a service. Without one, a restart loses
  the DB.

The default file is `compose.yaml` (preferred) or `compose.yml`; legacy
`docker-compose.yml` still works. The lifecycle:

- `docker compose up` — builds images, creates networks and volumes, starts
  all services.
- `docker compose down` — stops and removes the services (named volumes
  survive by default; `down -v` removes them too).
- `docker compose ps` / `logs` — status and output of the stack.
- Projects: each Compose app is a named "project", which lets the same file
  run twice in isolation.

A minimal web+db stack:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://app:pw@db/app
    depends_on:
      - db
  db:
    image: postgres:17
    environment:
      - POSTGRES_PASSWORD=pw
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

`depends_on` only orders startup; it does **not** wait for Postgres to be
ready to accept connections — the app must retry, or you add a healthcheck
that Compose waits on.

## How it fails (review checklist)

- **No volume on the database** — `docker compose down && up` wipes your data;
  declare a named volume or you lose the DB on every restart.
- **`depends_on` mistaken for readiness** — the api starts before Postgres can
  accept connections and crashes; add a healthcheck (`condition:
  service_healthy`) or retry in the app.
- **Hardcoded hosts/ports instead of service names** — containers are
  reachable by their service name on the Compose network, not by
  `localhost`; `localhost` inside the `api` container is the container
  itself, not your host's Postgres.
- **Ignoring secrets** — `environment:` values land in the compose file and
  repo history; the Spec's `secrets:` exists because plain env vars are not a
  secret store.
- **Building the world in dev** — mounting source as a volume for hot-reload
  is the dev trick; baking it into the image and fighting to rebuild is the
  failure.

## Build that proves it

The Dockerfile half is proven by [builds/production-deploy.md](../builds/production-deploy.md)
(and `containers-docker.md`'s drill). The Compose half has no build yet — the
drill below is the rep: stack two services with a named volume and watch the
data survive a `down`.

## Drill

Goal: prove `docker compose up` starts two services from one YAML, that they
reach each other by service name, and that a named volume keeps data across a
`down`.

Steps:
1. Dependency: Docker Desktop running, `docker compose version` works. In a
   scratch dir, save the minimal stack above (the `api`/`db` example) as
   `compose.yaml`. For `build: .` to work, put a trivial `Dockerfile`
   (`FROM python:3-slim\nCMD ["python", "-m", "http.server", "8000"]`) and a
   `hello.txt` next to it.
2. `docker compose up -d`, then `docker compose ps` — both services show
   `Up`, and `api` maps `8000`.
3. Prove service-name resolution: `docker compose exec api python3 -c "import
   socket; print(socket.gethostbyname('db'))"` — prints a private-IP address
   from the Compose network. That name is what `DATABASE_URL` uses.
4. Prove volume persistence: `docker compose exec db sh -c "echo hi >
   /var/lib/postgresql/data/keep.txt"`, then `docker compose down` and
   `docker compose up -d`, then `docker compose exec db cat
   /var/lib/postgresql/data/keep.txt` — still prints `hi`.

Self-check (pass/fail — run it alone):
- Step 2 shows two `Up` services and `ps` lists both.
- Step 3 resolves `db` to a Compose-network IP (not `127.0.0.1`) — you can
  explain why the app uses that name as its DB host.
- Step 4's file survives `down` (named volume) — and if you rerun step 4 with
  `down -v`, the file is gone: that `-v` is the footgun that wipes dev data.

Why this matters: the full local stack — app + DB + cache — is the shape of
every real backend, and "why is my data gone after restart" and "why can't the
app reach the DB" are the two junior failures Compose either fixes or silently
causes.

## Further reading
- Docker Docs, https://docs.docker.com/compose/ — "Docker Compose" (fetched
  Aug 6 2026)
- Docker Docs, https://docs.docker.com/compose/intro/compose-application-model/ —
  "How Compose works" (application model; fetched Aug 6 2026)
- Docker Docs, https://docs.docker.com/reference/compose-file/ — "Compose file
  reference" (fetched Aug 6 2026)
