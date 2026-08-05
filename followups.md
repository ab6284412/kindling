# Follow-ups

Standing items that must be re-checked before they're cited as current. Every
digest session: re-test anything here, update its status, and add any new open
questions that surfaced.

| Topic | Last checked | Status | Next action |
|---|---|---|---|
| openai.com/news | 2026-08-03 | Blocked (JS shell / bot challenge) | Re-test each pull (`python3 pull.py` flags if reachable); fall back to HN/Lobsters mirrors |
| changelog.com weekly news | 2026-08-03 | Paused/reorged (homepage through #185, Apr 2026) | Verify whether weekly news restarted before citing as current |
| Postgres for stage 5/6 checks | 2026-08-05 | Works on local `postgres:17-alpine` (`docker run -d --name techresearch-pg -e POSTGRES_PASSWORD=p -p 5432:5432 postgres:17-alpine`); `postgres:16` pull timed out on this network | Use the local image; run checks with `DATABASE_URL="postgresql://postgres:p@localhost:5432/postgres"` |
| shithub.us (Plan 9 sources) | 2026-08-05 | Unreachable, then 404 on the `/moody/wg` path | Dead link annotated in Aug 4 digest; re-fetch before citing anything from shithub |
| github.com/david-g-3654/homebench | 2026-08-05 | Repo 404 (taken down same day as HN post) | Provenance preserved via HN thread item?id=49166308; do not restore the dead URL |
| Port 8021 (macOS, localhost) | 2026-08-05 | Held by a launchd-adopted orphan; `lsof`/`kill` can't free it | background-worker check uses 8022; don't reuse 8021 for other checks |
| Check hardening (Aug 5 2026) | 2026-08-05 | New checks live: python_foundation order/import-safety/rm-99; http-server odd-length 411; auth bad-email/expired/on_startup-restart; storage-cache cache-presence + cascade; worker now HTTP-POSTs webhook under real uvicorn (8022); production-deploy SIGTERM removed + pytest suite + root `.github/workflows/production-deploy.yml` | Re-run `verify.py all` (expect exit 3 when the portal holds :8000) after any solution/spec change |
