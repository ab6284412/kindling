# Concepts

The textbook. One article per concept a junior backend developer must actually
understand, organized by learning stage (see [learning.md](../learning.md)):
1 = language foundation, 2 = request/response core, 3 = API design & reliability,
4 = auth & security, 5 = state & storage, 6 = async work & concurrency,
7 = production, ops & scale (the DSA/interview prep track sits outside the
stages).

Every concept article is **AI-drafted and must be verified against its Further reading**
— that's the point of the Provenance mark. Human-authored sources are always
credited. If a claim survives only in this repo and not in a cited source, it
is a mistake waiting to be found.

The catalogue below mirrors the [roadmap.sh Backend Roadmap](https://roadmap.sh/backend)
(fetched Aug 3 2026): 23 roadmap steps, plus the roadmap's Security and
Authentication clusters treated as their own articles. Step → concept mapping
follows the roadmap's own grouping; where a roadmap step spans multiple
articles (e.g. NoSQL databases), the article covers the whole step.

## Core five (the workspace's stack, in learning order)

| Stage | Concept | Article | Build (prove it by hand) |
|---|---|---|---|
| 1 | Python import system | [python-import-system.md](python-import-system.md) | [python-from-zero](../builds/python-from-zero.md) |
| 2 | HTTP request/response model | [http-request-response.md](http-request-response.md) | [http-server](../builds/http-server.md) |
| 3 | Dependency injection in FastAPI | [fastapi-dependency-injection.md](fastapi-dependency-injection.md) | [fastapi-crud](../builds/fastapi-crud.md) |
| 4 | Authentication & security | [authentication-authorization.md](authentication-authorization.md) | [auth-security](../builds/auth-security.md) |
| 5 | Transactions & ACID | [transactions-acid.md](transactions-acid.md) | [storage-cache](../builds/storage-cache.md) |
| 6 | Async work & concurrency | [concurrency-parallelism.md](concurrency-parallelism.md) | [background-worker](../builds/background-worker.md) |
| 7 | Containers & Docker for a Python API | [containers-docker.md](containers-docker.md) | [production-deploy](../builds/production-deploy.md) |

## Roadmap catalogue (all 23 steps + security/auth)

| # | Roadmap step | Article |
|---|---|---|
| 1 | Introduction (how the web works) | [introduction-web-basics.md](introduction-web-basics.md) |
| 2 | Pick a Backend Language | [backend-languages.md](backend-languages.md) |
| 3 | Version Control Systems | [version-control-git.md](version-control-git.md) |
| 4 | Repo Hosting Services | [repo-hosting-services.md](repo-hosting-services.md) |
| 5 | Relational Databases | [relational-databases.md](relational-databases.md) |
| 6 | NoSQL Databases | [nosql-databases.md](nosql-databases.md) |
| 7 | More about Databases | [more-about-databases.md](more-about-databases.md) |
| 8 | Scaling Databases | [scaling-databases.md](scaling-databases.md) |
| 9 | Learn about APIs | [apis-rest-graphql-grpc.md](apis-rest-graphql-grpc.md) |
| 10 | Caching | [caching.md](caching.md) |
| 11 | Testing | [testing.md](testing.md) |
| 12 | CI / CD | [ci-cd.md](ci-cd.md) |
| 13 | Architectural Patterns | [architectural-patterns.md](architectural-patterns.md) |
| 14 | Message Brokers | [message-brokers.md](message-brokers.md) |
| 15 | Learn about Web Servers | [web-servers.md](web-servers.md) |
| 16 | Building For Scale | [building-for-scale.md](building-for-scale.md) |
| 17 | Security (roadmap cluster) | [web-security.md](web-security.md) |
| 18 | Authentication (roadmap cluster) | [authentication-authorization.md](authentication-authorization.md) |
| 19 | Real-Time Data | [real-time-data.md](real-time-data.md) |
| 20 | Search Engines | [search-engines.md](search-engines.md) |
| 21 | Frontend Basics | [frontend-basics.md](frontend-basics.md) |
| 22 | Learn the Basics (projects) | [learn-the-basics-projects.md](learn-the-basics-projects.md) |
| 23 | AI Assisted Coding | [ai-assisted-coding.md](ai-assisted-coding.md) |
| 24 | Applications (AI features) | [ai-applications.md](ai-applications.md) |
| 25 | Integration Patterns (AI) | [ai-integration-patterns.md](ai-integration-patterns.md) |

## Workspace additions (not roadmap steps)

Workspace additions indexed in the video-mapped or Core-five tables above, not
in the roadmap catalogue — they are not roadmap steps:

`backend-first-principles.md`, `what-is-a-backend.md`, `http-request-response.md`,
`routing.md`, `serialization.md`, `validations-transformations.md`,
`application-layers.md`, `error-handling-fault-tolerance.md`,
`configuration-management.md`, `observability.md`, `graceful-shutdown.md`,
`concurrency-parallelism.md`, `python-import-system.md`,
`fastapi-dependency-injection.md`, `containers-docker.md`, `transactions-acid.md`

## Video-mapped concepts (Sriniously ▶1–▶23)

Each playlist video now has a dedicated concept note; the video's YouTube URL is
the first line of its `## Further reading`. `▶N` = playlist position (see
[learning.md](../learning.md) for the credit legend).

| ▶ | Video | Concept |
|---|---|---|
| 1, 2, 4 | Roadmap / walk the path / why first principles | [backend-first-principles.md](backend-first-principles.md) |
| 3 | What is a Backend | [what-is-a-backend.md](what-is-a-backend.md) |
| 5 | Understanding HTTP | [http-request-response.md](http-request-response.md) |
| 6 | What is Routing | [routing.md](routing.md) |
| 7 | Serialization and Deserialization | [serialization.md](serialization.md) |
| 8 | Authentication and authorization | [authentication-authorization.md](authentication-authorization.md) |
| 9 | Validations and transformations | [validations-transformations.md](validations-transformations.md) |
| 10 | Controllers, services, repositories, middleware, request context | [application-layers.md](application-layers.md) |
| 11 | Complete REST API Design | [apis-rest-graphql-grpc.md](apis-rest-graphql-grpc.md) |
| 12 | Mastering Databases with Postgres | [relational-databases.md](relational-databases.md) |
| 13 | Caching | [caching.md](caching.md) |
| 14 | Task queues and background jobs | [message-brokers.md](message-brokers.md) |
| 15 | Full text search (Elasticsearch) | [search-engines.md](search-engines.md) |
| 16 | Error handling & fault tolerance | [error-handling-fault-tolerance.md](error-handling-fault-tolerance.md) |
| 17 | Production-grade configuration | [configuration-management.md](configuration-management.md) |
| 18 | Logging, monitoring, observability | [observability.md](observability.md) |
| 19 | Graceful shutdown | [graceful-shutdown.md](graceful-shutdown.md) |
| 20 | Backend security | [web-security.md](web-security.md) |
| 21, 22 | Scaling & performance 1/2 | [building-for-scale.md](building-for-scale.md) |
| 23 | Concurrency: IO- vs CPU-bound | [concurrency-parallelism.md](concurrency-parallelism.md) |

## Rules for adding a concept

- Copy `templates/concept.md`. Header must carry `Provenance` and `Credits`.
- Every factual claim must trace to a `## Further reading` URL with a date. No source,
  no concept.
- A concept without a `Build` link is theory; add a build when the concept can
  be constructed by hand, and add a `## Drill` section for the short
  lesson-specific rep.
