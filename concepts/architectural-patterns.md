# Architectural patterns
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, The Twelve-Factor App authors, Fowler

## What it is

The roadmap's thirteenth step: the high-level shapes a backend system can
take — **monolith, SOA, microservices, service mesh, serverless, and
twelve-factor apps**. This is the "how do I organize the whole system"
level, above any single service.

## The concepts

- **Monolith** — one deployable containing everything; simplest, most
  reliable, and the right default for most apps.
- **SOA** — service-oriented architecture: large services with shared
  contracts (usually SOAP/XML; the older sibling of microservices).
- **Microservices** — many small independently-deployed services, each
  owning its data; buys team scale, pays with distributed-systems tax.
- **Service mesh** — a dedicated infrastructure layer (sidecar proxies) that
  handles service-to-service traffic, retries, and observability for you.
- **Serverless** — deploy functions, not servers; the platform scales to
  zero and handles the infra (see `building-for-scale.md`).
- **Twelve-factor apps** — a checklist for building portable, cloud-ready
  apps: config in env vars, stateless processes, disposable, etc.

## How it works

Each pattern is a tradeoff packaged as a name. The lazy-senior principle
from this workspace's guardrails maps directly: **start monolith** — the
modular-monolith with clean internal seams migrates to microservices later;
a distributed monolith (microservices wired badly) is the worst of both.

## How it fails (review checklist)

- **Microservices as resume bait** — distributed systems fail in
  un-reproducible ways; a monolith of 50k LOC is manageable, a network
  partition is not.
- **Shared database between services** — the #1 way "microservices" stop
  being independent; each service owns its data or it isn't micro.
- **Skipping twelve-factor** — config in the code, state in the process;
  then the app can't run on a second machine, let alone autoscale.
- **Service mesh as a first step** — you need a *service* before a *mesh*;
  it's operational overhead, not a feature.

## Build that proves it

No build yet. The drill: take the roadmap's twelve-factor list and score an
existing app of yours (this `web/` app counts) against all twelve factors,
one by one.

## Drill

Goal: prove twelve-factor's "config in env vars" by running one unchanged
script under three different environments. Stdlib only.

Steps:
1. Save this as `config_drill.py`:
   ```python
   import os
   def db_url():
       return os.environ.get("DATABASE_URL", "postgres://localhost/dev")
   def main():
       print("connecting to", db_url())
   if __name__ == "__main__":
       main()
   ```
2. Run it three ways without editing the file:
   ```bash
   python3 config_drill.py
   DATABASE_URL=postgres://prod-eu python3 config_drill.py
   DATABASE_URL=postgres://staging python3 config_drill.py
   ```
3. Now write the "hardcoded" version: replace `db_url()` with
   `return "postgres://localhost/dev"` and re-run the three commands — the
   second and third now connect to the wrong database silently.

Self-check (pass/fail — run it alone): the three env-var runs print three
*different* URLs from the same file (pass), and the hardcoded version prints
the same URL for all three even when `DATABASE_URL` is set (fail — that's the
twelve-factor violation made visible). You passed if you can say which app
runs on a second machine.

Why this matters: config baked into code is why "it works on my machine" —
env-var config is what lets the same image deploy to dev, staging, and prod.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Architectural Patterns" step
  (fetched Aug 3 2026)
- Adam Wiggins et al., https://12factor.net/ — "The Twelve-Factor App"
  (fetched Aug 3 2026)
- Martin Fowler, https://martinfowler.com/bliki/CircuitBreaker.html —
  "CircuitBreaker" (fetched Aug 3 2026)
