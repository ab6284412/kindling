# Learning path: backend from first principles
Created 2026-08-03 · restructured 2026-08-03
Provenance: AI-drafted
Credits: Sriniously (@sriniously) — "Backend from first principles" playlist
(23 videos, Sep 2024–Dec 2025), the concept source for this path.

Purpose: each concept and knowledge note embeds a short `## Drill` rep pulled
from the news. This is the structured curriculum for fundamentals — the stuff
that doesn't change with the news cycle. Free, project-based, verified Aug 3 2026.

Restructured Aug 3 2026 from a tool-centric list (Python → SQL → HTTP →
FastAPI → ops) into a **principle-first path from zero**: stages are named by
the question they answer, not the tool. FastAPI is a vehicle inside stage 3,
not the path. Every concept credits the playlist video that teaches it (`▶N`,
see the legend at the bottom).

## The path (from zero, in order, ~5-10 hrs/week)

Tick a stage when you've completed its project and passed the stage's own
certification/test — not when you've watched the videos.

### 1. Language foundation: Python + tooling — from zero `[ ]`
The prerequisite before any backend: write, run, and debug Python programs and
version your work with git. Every later stage assumes you can do this without
looking it up.
- freeCodeCamp [Python Certification (v9)](https://www.freecodecamp.org/learn/python-v9/)
  (free, project-based cert: from zero through OOP, data structures and
  algorithms). **Tick: the 5 required projects + pass the certification exam.**
- Supplement: Exercism Python track (fast feedback, small problems). SQLZoo
  waits for stage 5.
- Git + GitHub basics: add/commit/push, branch, pull request.
- Concepts: [concepts/python-import-system.md](concepts/python-import-system.md) · Drill: the `## Drill` in that note
- DSA practice: pick these up in the certification's later courses — Linear Data
  Structures, Algorithms, Graphs & Trees, Dynamic Programming — then drill the
  same patterns here: [dsa/big-o-notation.md](dsa/big-o-notation.md), [dsa/arrays-strings.md](dsa/arrays-strings.md),
  [dsa/recursion-backtracking.md](dsa/recursion-backtracking.md), [dsa/hashing.md](dsa/hashing.md)
- Roadmap steps: Pick a Backend Language ([concepts/backend-languages.md](concepts/backend-languages.md)),
  Version Control ([concepts/version-control-git.md](concepts/version-control-git.md)), Repo Hosting
  ([concepts/repo-hosting-services.md](concepts/repo-hosting-services.md)), Learn the Basics (projects)
  ([concepts/learn-the-basics-projects.md](concepts/learn-the-basics-projects.md))

### 2. The request/response core `[ ]`
*"How does a request become a response?"* The question every backend answers:
HTTP protocol, routing, serialization, validation, and the layered request
lifecycle. Build the whole thing from raw sockets so no framework hides it.
- Watch: ▶3 what a backend is ([concepts/what-is-a-backend.md](concepts/what-is-a-backend.md)),
  ▶5 HTTP ([concepts/http-request-response.md](concepts/http-request-response.md)), ▶6 routing
  ([concepts/routing.md](concepts/routing.md)), ▶7 serialization
  ([concepts/serialization.md](concepts/serialization.md)), ▶9 validation & transformation
  ([concepts/validations-transformations.md](concepts/validations-transformations.md)), ▶10
  controllers/services/repositories/middleware/request context
  ([concepts/application-layers.md](concepts/application-layers.md)).
- **Tick: [builds/http-server.md](builds/http-server.md)** — a stdlib-socket HTTP/1.1 server, no
  framework.
- Concepts: [concepts/introduction-web-basics.md](concepts/introduction-web-basics.md), [concepts/http-request-response.md](concepts/http-request-response.md)
- DSA practice: [dsa/stack-queue.md](dsa/stack-queue.md) (deque as the workhorse buffer)
- Roadmap steps: Introduction ([concepts/introduction-web-basics.md](concepts/introduction-web-basics.md))

### 3. API design & reliability `[ ]`
*"How do you make the exchange documented, correct, and predictable?"* REST
design, error handling, and fault tolerance. Implemented in FastAPI — the
vehicle here, not the topic.
- Watch: ▶11 Complete REST API Design ([concepts/apis-rest-graphql-grpc.md](concepts/apis-rest-graphql-grpc.md)),
  ▶16 Error Handling and Building Fault Tolerant Systems
  ([concepts/error-handling-fault-tolerance.md](concepts/error-handling-fault-tolerance.md)).
- **Tick: [builds/fastapi-crud.md](builds/fastapi-crud.md)** — CRUD API with a dependency-injected DB
  session, hand-written SQL, and error handling.
- Concepts: [concepts/apis-rest-graphql-grpc.md](concepts/apis-rest-graphql-grpc.md), [concepts/architectural-patterns.md](concepts/architectural-patterns.md),
  [concepts/testing.md](concepts/testing.md), [concepts/fastapi-dependency-injection.md](concepts/fastapi-dependency-injection.md) ·
  Drill: the `## Drill` in [concepts/fastapi-dependency-injection.md](concepts/fastapi-dependency-injection.md)
- DSA practice: [dsa/hashing.md](dsa/hashing.md), [dsa/two-pointers.md](dsa/two-pointers.md) (dict/set and in-place
  passes in request logic)
- Roadmap steps: Learn about APIs ([concepts/apis-rest-graphql-grpc.md](concepts/apis-rest-graphql-grpc.md)),
  Architectural Patterns ([concepts/architectural-patterns.md](concepts/architectural-patterns.md)), Testing
  ([concepts/testing.md](concepts/testing.md))

### 4. Authentication & security `[ ]`
*"Who is calling, and what are they allowed to do?"* Authentication vs
authorization, password handling, tokens, and the OWASP failure classes that
get APIs pwned.
- Watch: ▶8 Authentication and authorization
  ([concepts/authentication-authorization.md](concepts/authentication-authorization.md)), ▶20 Backend
  Security ([concepts/web-security.md](concepts/web-security.md)).
- **Tick: [builds/auth-security.md](builds/auth-security.md)** — password hashing, token login,
  ownership checks, and an OWASP review.
- Concepts: [concepts/authentication-authorization.md](concepts/authentication-authorization.md), [concepts/web-security.md](concepts/web-security.md)
- DSA practice: [dsa/hashing.md](dsa/hashing.md) (hash functions, collisions, salts)
- Roadmap steps: Security ([concepts/web-security.md](concepts/web-security.md)), Authentication
  ([concepts/authentication-authorization.md](concepts/authentication-authorization.md))

### 5. State & storage `[ ]`
*"Where does data live, and how do you get it back fast?"* Relational modeling,
 transactions/ACID, caching, and full-text search — the systems that outlive
 any process.
- Watch: ▶12 Mastering Databases with Postgres
  ([concepts/relational-databases.md](concepts/relational-databases.md)), ▶13 Caching
  ([concepts/caching.md](concepts/caching.md)), ▶15 Full text search using Elasticsearch
  ([concepts/search-engines.md](concepts/search-engines.md)).
- **Tick: [builds/storage-cache.md](builds/storage-cache.md)** — Postgres behind the CRUD API plus a
  cache layer with correct invalidation.
- Concepts: [concepts/relational-databases.md](concepts/relational-databases.md), [concepts/nosql-databases.md](concepts/nosql-databases.md),
  [concepts/more-about-databases.md](concepts/more-about-databases.md), [concepts/transactions-acid.md](concepts/transactions-acid.md) ·
  Drill: the `## Drill` in [concepts/transactions-acid.md](concepts/transactions-acid.md), [concepts/caching.md](concepts/caching.md),
  [concepts/search-engines.md](concepts/search-engines.md)
- DSA practice: [dsa/binary-search.md](dsa/binary-search.md), [dsa/trees.md](dsa/trees.md) (index lookup is the
  halving search over a B-tree)
- Roadmap steps: Relational ([concepts/relational-databases.md](concepts/relational-databases.md)), NoSQL
  ([concepts/nosql-databases.md](concepts/nosql-databases.md)), More about Databases
  ([concepts/more-about-databases.md](concepts/more-about-databases.md)), Search Engines
  ([concepts/search-engines.md](concepts/search-engines.md))

### 6. Async work & concurrency `[ ]`
*"What if a request can't finish synchronously?"* Background jobs, task queues,
 and knowing IO-bound from CPU-bound — when threads/async help and when they
 don't.
- Watch: ▶14 Task queues and background jobs ([concepts/message-brokers.md](concepts/message-brokers.md)),
  ▶23 Concurrency & Parallelism ([concepts/concurrency-parallelism.md](concepts/concurrency-parallelism.md)).
- **Tick: [builds/background-worker.md](builds/background-worker.md)** — a slow operation moved off the
  request path into a queue + worker, with a completion webhook.
- Concepts: [concepts/message-brokers.md](concepts/message-brokers.md), [concepts/real-time-data.md](concepts/real-time-data.md)
- DSA practice: [dsa/heaps.md](dsa/heaps.md) (priority queues for job scheduling),
  [dsa/graphs.md](dsa/graphs.md) (dependency graphs)
- Roadmap steps: Message Brokers ([concepts/message-brokers.md](concepts/message-brokers.md)), Real-Time
  Data ([concepts/real-time-data.md](concepts/real-time-data.md))

### 7. Production, ops & scale `[ ]`
*"How do you run it, watch it, keep it alive, and grow it?"* Config management,
 observability, graceful shutdown, and performance engineering — the layer that
 turns a working API into a service.
- Watch: ▶17 Production-grade Configuration Management
  ([concepts/configuration-management.md](concepts/configuration-management.md)), ▶18 Logging,
  Monitoring and Observability ([concepts/observability.md](concepts/observability.md)), ▶19 Graceful
  Shutdown ([concepts/graceful-shutdown.md](concepts/graceful-shutdown.md)), ▶21 Backend Scaling and
  Performance Part-1 / ▶22 Part-2
  ([concepts/building-for-scale.md](concepts/building-for-scale.md)).
- **Tick: [builds/production-deploy.md](builds/production-deploy.md)** — containerize, env config, CI,
  logging/metrics, graceful shutdown, then load-test → find the bottleneck →
  fix → re-measure.
- Concepts: [concepts/web-servers.md](concepts/web-servers.md), [concepts/containers-docker.md](concepts/containers-docker.md) ·
  Drill: the `## Drill` in [concepts/containers-docker.md](concepts/containers-docker.md), [concepts/ci-cd.md](concepts/ci-cd.md),
  [concepts/scaling-databases.md](concepts/scaling-databases.md), [concepts/building-for-scale.md](concepts/building-for-scale.md)
- DSA practice: [dsa/graphs.md](dsa/graphs.md) (CI/dependency graphs), [dsa/heaps.md](dsa/heaps.md)
  (priority queues for job scheduling)
- Roadmap steps: Web Servers ([concepts/web-servers.md](concepts/web-servers.md)), CI/CD
  ([concepts/ci-cd.md](concepts/ci-cd.md)), Scaling Databases ([concepts/scaling-databases.md](concepts/scaling-databases.md)),
  Building For Scale ([concepts/building-for-scale.md](concepts/building-for-scale.md))

## Walk the path first

Videos ▶1 (the roadmap), ▶2 (what the end goal looks like), and ▶4 (why first
 principles is the strategy) aren't a stage — they're the path's own rationale
 ([concepts/backend-first-principles.md](concepts/backend-first-principles.md)).
Watch them before starting stage 1, and re-watch ▶4 when the tools feel like
the point.

## Parallel track (not a stage — run alongside)

DSA + interview prep — patterns-first (NeetCode/Blind-75 style), the 13
 patterns ordered in [dsa/README.md](dsa/README.md). Run while applying for jobs; the
 fundamentals above make the algorithms mean something.
- Prep companions: [soft-skills/](soft-skills/) (debugging, questions, review
  etiquette, plus the [jargon glossary](soft-skills/communication-skills/jargon/)),
  [interview puzzles](dsa/puzzles/) (interview-style reasoning problems, tied
  into the pattern notes).
- Optional roadmap steps: Frontend Basics ([concepts/frontend-basics.md](concepts/frontend-basics.md)),
  AI Assisted Coding ([concepts/ai-assisted-coding.md](concepts/ai-assisted-coding.md)), AI Applications +
  integration patterns ([concepts/ai-applications.md](concepts/ai-applications.md),
  [concepts/ai-integration-patterns.md](concepts/ai-integration-patterns.md)).

## How it connects to the workspace

- Knowledge note → drill is the *short rep* for a news lesson; the matching
  path stage is the *deep practice* for the underlying fundamental.
- Concepts are the textbook for each stage; builds prove a concept by hand.
- Habit: after each digest, pick one news item and find which path stage teaches
  it (e.g. "Qwen speed vs quality" → stage 7, measure latency in your own API),
  and add a falsifiable row to [predictions.md](predictions.md) when it signals
  a trend.

## Credit legend (▶N)

Every concept above traces to a specific video by **Sriniously (@sriniously)**
in the "Backend from first principles" playlist (23 videos, Sep 2024–Dec 2025).
`▶N` = playlist position N (the table below resolves it). The author's own
labels (e.g. "21.1/21.2", then "22") don't line up with run order, so position
numbers are used:

| ▶ | Video (Sriniously) | URL | Published |
|---|---|---|---|
| 1 | Roadmap for backend from first principles | https://www.youtube.com/watch?v=0Rwb4Xmlcwc | Sep 23, 2024 |
| 2 | Walk the path of a true backend engineer | https://www.youtube.com/watch?v=3qFjZbFRSAU | Sep 23, 2024 |
| 3 | What is a Backend, how they work and why | https://www.youtube.com/watch?v=6Ss4dJD9Kzg | Sep 24, 2024 |
| 4 | Benefits of learning backend from first principles | https://www.youtube.com/watch?v=6fqZs5Z3k9A | Sep 25, 2024 |
| 5 | Understanding HTTP for backend engineers | https://www.youtube.com/watch?v=a3C1DMswClQ | Sep 27, 2024 |
| 6 | What is Routing in Backend? | https://www.youtube.com/watch?v=SubuU1iOC2s | Dec 9, 2024 |
| 7 | Serialization and Deserialization | https://www.youtube.com/watch?v=vzg90tY3uM0 | Dec 11, 2024 |
| 8 | Authentication and authorization | https://www.youtube.com/watch?v=A95rliroC8Q | Dec 23, 2024 |
| 9 | Validations and transformations | https://www.youtube.com/watch?v=qedj_JjjL-U | Jan 12, 2025 |
| 10 | Controllers, services, repositories, middlewares, request context | https://www.youtube.com/watch?v=hyc-7w3pee8 | Jan 16, 2025 |
| 11 | Complete REST API Design | https://www.youtube.com/watch?v=RG6q57DwV8Y | Feb 8, 2025 |
| 12 | Mastering Databases with Postgres | https://www.youtube.com/watch?v=F7Vwp2Xo5Do | Mar 3, 2025 |
| 13 | Caching, the secret behind it all | https://www.youtube.com/watch?v=estH64OkwxU | Mar 5, 2025 |
| 14 | Task queues and background jobs | https://www.youtube.com/watch?v=r-nQsyguU1Y | Apr 16, 2025 |
| 15 | Full text search using Elasticsearch | https://www.youtube.com/watch?v=7_sovzAhRSM | Jul 5, 2025 |
| 16 | Error Handling and Building Fault Tolerant Systems | https://www.youtube.com/watch?v=8NaM_9aKS24 | Jul 8, 2025 |
| 17 | Production-grade Configuration Management | https://www.youtube.com/watch?v=GR9NtirPXyc | Jul 24, 2025 |
| 18 | Logging, Monitoring and Observability | https://www.youtube.com/watch?v=5PEuwgLOQQM | Jul 26, 2025 |
| 19 | Graceful Shutdown | https://www.youtube.com/watch?v=6rfBgphiCWM | Sep 19, 2025 |
| 20 | Backend Security: Everything You Need | https://www.youtube.com/watch?v=xB1C1xZZW4k | Dec 14, 2025 |
| 21 | Backend Scaling and Performance Part-1 (21.1) | https://www.youtube.com/watch?v=z7kt_p44rjs | Dec 14, 2025 |
| 22 | Backend Scaling and Performance Part-2 (21.2) | https://www.youtube.com/watch?v=sOhAopEwjH4 | Dec 28, 2025 |
| 23 | Concurrency & Parallelism: IO Bound vs CPU Bound | https://www.youtube.com/watch?v=bs9MEYRTA30 | Dec 31, 2025 |

## Further reading (verified reachable, Aug 3 2026)
- Playlist (primary concept source): https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1 — Sriniously,
  "Backend from first principles" (23 videos, Sep 2024–Dec 2025)
- https://www.freecodecamp.org/learn/python-v9/ — Python Certification (v9) cert (stage 1)
- https://exercism.org/tracks/python — free Python track
- https://sqlzoo.net/ — free SQL exercises
- https://fastapi.tiangolo.com/ — official FastAPI tutorial (the vehicle in stage 3)
- https://www.fullstackopen.com/ — free University of Helsinki + DevOps with Docker
- https://roadmap.sh/backend — backend roadmap (navigation, not a course)