# Learn about web servers
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Nginx docs

## What it is

The roadmap's fifteenth step: the server software that actually answers HTTP
requests — **Nginx, Caddy, Apache, and MS IIS**, plus the container
technology **LXC**. For a FastAPI dev: your app is the logic, the web server
is the front door (TLS, static files, proxying).

## The concepts

- **Nginx** — high-performance, event-driven reverse proxy and static-file
  server; the de-facto default front door in front of Python apps.
- **Caddy** — automatic HTTPS (Let's Encrypt out of the box), simpler config
  than Nginx, younger.
- **Apache** — the classic HTTP server, still massive in legacy/`mod_php`
  land.
- **MS IIS** — Microsoft's web server (Windows world).
- **LXC** — OS-level containerization (namespace + cgroup isolation); the
  technology Docker was built on (see `containers-docker.md`).

## How it works

Two roles, both relevant: **static server** (serves files fast) and
**reverse proxy** (accepts client connections, terminates TLS, forwards to
your app, balances load). Python's dev server is explicitly not for
production; Nginx + Gunicorn/uvicorn is the classic FastAPI stack. The web
server is not the app — confusing the two is the classic junior failure.

## How it fails (review checklist)

- **Productionizing the dev server** — `uvicorn app:app` alone has no TLS,
  no workers, no static files; put a real server in front.
- **Nginx as a magic box** — config errors return 502/504 with no intuition
  about why; learn the proxy pipeline (upstream, headers, timeouts).
- **Web server ≠ app server** — Nginx terminates TLS and forwards; your app
  still owns the logic. Load *shifts*, it doesn't disappear.
- **Forgetting LXC/Docker differences** — containers share the host kernel;
  a container is a process with isolation, not a lightweight VM.

## Build that proves it

No build yet. The drill: put Nginx (in Docker) in front of this workspace's
FastAPI `web/` app — terminate TLS with a self-signed cert, proxy `/` to the
app, serve a static file directly from Nginx, and observe the `X-Forwarded-*`
headers your app sees.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Learn about Web Servers" step
  (fetched Aug 3 2026)
- Nginx docs, https://nginx.org/en/docs/ — "nginx documentation"
  (fetched Aug 3 2026)
