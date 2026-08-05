# Backend from first principles: the meta case
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

A strategy for learning backend engineering: don't collect tools, learn the
*causes*. First principles means you can derive behavior instead of memorizing
it — when you know why HTTP is stateless, a framework's routing table stops
being magic. Sriniously's roadmap (▶1), the walk-through of the path (▶2), and
the rationale video (▶4) frame the whole curriculum this workspace uses.

## How it works

- **▶1 Roadmap** — the full map: what to learn in what order, from request →
  response → API design → auth → storage → async → production.
- **▶2 Walk the path** — what a backend engineer actually does day to day, the
  end goal that makes the early stages concrete.
- **▶4 Benefits of first principles** — why understanding the underlying
  mechanism beats knowing framework APIs: the framework becomes an instance,
  not a dependency.

## How it fails

- Treating the *tools* (FastAPI, Postgres, Docker) as the curriculum. They're
  vehicles; the concepts they implement are the point.
- Skipping the "why" videos because they have no code. They're the reference
  point that stops you chasing new frameworks every month.
- Learning stages in isolation — the path only compounds if stage 1 is actually
  solid before stage 2.

## Build that proves it

No build; this is the ordering rationale, not a mechanism. Proof is completing
[learning.md](../learning.md) and being able to answer "why this and not that"
at each tick.

## Drill

Goal: prove you can derive a framework behavior from first principles instead
of memorizing its API.

Steps:
1. In a scratch dir, open a new file `derive.txt`. Without any web or docs,
   write the causal chain answering: "why can't a FastAPI app 'remember' a
   logged-in user unless the request itself carries identity?" Start from "HTTP
   is stateless" and end at "so identity must travel with every request".
2. Verify the load-bearing link — that a fresh request really carries nothing.
   Run `python3 -m http.server 8125` in the scratch dir, then in another
   terminal `curl -v http://localhost:8125/ 2>&1 | grep '^>'` — the request
   lines contain no `Cookie` header on first hit.
3. Now simulate identity: `curl -v -H "Cookie: session=abc" http://localhost:8125/ 2>&1 | grep '^>'`
   — the request now carries exactly the header the app would key off.

Self-check (pass/fail):
- `derive.txt` chains at least 3 causes (stateless → no server memory →
  request must carry identity) and you can name which link cookies implement.
- Step 2's `grep '^>'` shows zero `Cookie` header; step 3 shows exactly
  `Cookie: session=abc`.
- You did not open a framework doc during steps 1–3.

Why this matters: deriving beats memorizing — when FastAPI's behavior surprises
you, you can now trace it to HTTP instead of calling it a framework quirk.

## Further reading
- Sriniously, "Backend from first principles" — https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1 (Sep 23 2024)
- Sriniously, ▶1 Roadmap for backend from first principles — https://www.youtube.com/watch?v=0Rwb4Xmlcwc (Sep 23, 2024)
- Sriniously, ▶2 Walk the path of a true backend engineer — https://www.youtube.com/watch?v=3qFjZbFRSAU (Sep 23, 2024)
- Sriniously, ▶4 Benefits of learning backend from first principles — https://www.youtube.com/watch?v=6fqZs5Z3k9A (Sep 25, 2024)
