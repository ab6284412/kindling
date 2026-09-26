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

The catalogue below is ordered as the **learning roadmap** — the same stage
sequence as [learning.md](../learning.md), not roadmap.sh's number order. Every
roadmap step keeps its step number (`#`) for roadmap reference; `—` marks a
workspace addition (a concept added beyond the roadmap, indexed as its own
article). The Subtopics column lists each step's child nodes from the
[roadmap.sh Backend Roadmap](https://roadmap.sh/backend) JSON (fetched Aug 6 2026);
workspace additions carry no roadmap subtopics.

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

## Learning roadmap (all concepts, in stage order)

| Stage | # | Concept | Subtopics | Article |
|---|---|---|---|---|
| Pre-path | — | Backend from first principles | ▶1 roadmap, ▶2 walk the path, ▶4 why first principles | [backend-first-principles.md](backend-first-principles.md) |
| **1 · Language foundation** | — | Python import system | modules, packages, `sys.path`, relative imports, `__main__` | [python-import-system.md](python-import-system.md) |
| | 2 | Pick a Backend Language | Python, Java, JavaScript, Go, Ruby, C#, PHP, Rust | [backend-languages.md](backend-languages.md) |
| | 3 | Version Control Systems | Git | [version-control-git.md](version-control-git.md) |
| | 4 | Repo Hosting Services | GitHub, GitLab | [repo-hosting-services.md](repo-hosting-services.md) |
| | 22 | Learn the Basics (projects) | Beginner/Intermediate project ideas, How LLMs work, AI vs Traditional Coding, Embeddings, Vectors | [learn-the-basics-projects.md](learn-the-basics-projects.md) |
| **2 · Request/response core** | 1 | Introduction (how the web works) | How the internet works, What is HTTP, What is a domain name, What is hosting, DNS, How browsers work | [introduction-web-basics.md](introduction-web-basics.md) |
| | — | What is a backend | the backend boundary, ▶3 | [what-is-a-backend.md](what-is-a-backend.md) |
| | — | HTTP request/response | request line, status codes, statelessness, ▶5 | [http-request-response.md](http-request-response.md) |
| | — | Routing | method+path → handler, route order, ▶6 | [routing.md](routing.md) |
| | — | Serialization & deserialization | JSON, schema-as-contract, ▶7 | [serialization.md](serialization.md) |
| | — | Validations & transformations | validate raw → transform, ▶9 | [validations-transformations.md](validations-transformations.md) |
| | — | Application layers | controllers/services/repositories/middleware/request context, ▶10 | [application-layers.md](application-layers.md) |
| **3 · API design & reliability** | 9 | Learn about APIs | REST, JSON APIs, SOAP, gRPC, GraphQL, Open API Specs | [apis-rest-graphql-grpc.md](apis-rest-graphql-grpc.md) |
| | 11 | Testing | Unit, Integration, Functional | [testing.md](testing.md) |
| | 13 | Architectural Patterns | Monolith, SOA, Microservices, Service Mesh, Twelve-Factor Apps, Serverless | [architectural-patterns.md](architectural-patterns.md) |
| | — | FastAPI dependency injection | `Depends()`, sub-dependencies, overrides | [fastapi-dependency-injection.md](fastapi-dependency-injection.md) |
| | — | Error handling & fault tolerance | timeouts, retries, backoff, circuit breakers, ▶16 | [error-handling-fault-tolerance.md](error-handling-fault-tolerance.md) |
| **4 · Auth & security** | 17 | Security (roadmap cluster) | OWASP Risks, HTTPS, SSL/TLS, CORS, CSP, Server Security, Hashing (MD5/SHA/scrypt/bcrypt) | [web-security.md](web-security.md) |
| | 18 | Authentication (roadmap cluster) | JWT, Basic/Token/Cookie Auth, OAuth, OpenID, SAML | [authentication-authorization.md](authentication-authorization.md) |
| **5 · State & storage** | 5 | Relational Databases | PostgreSQL, MySQL, MariaDB, SQLite, MS SQL, Oracle | [relational-databases.md](relational-databases.md) |
| | 6 | NoSQL Databases | Document/Key-Value/Graph/Column/Time-Series + engines (Redis, MongoDB, DynamoDB, Cassandra, Neo4j, InfluxDB, …) | [nosql-databases.md](nosql-databases.md) |
| | 7 | More about Databases | ORMs, Normalization, ACID, Transactions, Failure Modes, Profiling Performance, N+1 Problem, Migrations | [more-about-databases.md](more-about-databases.md) |
| | 10 | Caching | Redis, Memcached, HTTP Caching | [caching.md](caching.md) |
| | 20 | Search Engines | Elasticsearch, Solr | [search-engines.md](search-engines.md) |
| | — | Transactions & ACID | atomicity, isolation, durability, savepoints | [transactions-acid.md](transactions-acid.md) |
| **6 · Async work & concurrency** | 14 | Message Brokers | RabbitMQ, Kafka, LXC (containerization) | [message-brokers.md](message-brokers.md) |
| | 19 | Real-Time Data | WebSockets, Server-Sent Events, Long/Short Polling | [real-time-data.md](real-time-data.md) |
| | — | Concurrency & parallelism | IO- vs CPU-bound, GIL, threads/processes/async, ▶23 | [concurrency-parallelism.md](concurrency-parallelism.md) |
| **7 · Production, ops & scale** | 8 | Scaling Databases | Database Indexes, Data Replication, Sharding Strategies, CAP Theorem | [scaling-databases.md](scaling-databases.md) |
| | 12 | CI / CD | GitHub Actions, GitLab CI (pipeline automation) | [ci-cd.md](ci-cd.md) |
| | 15 | Learn about Web Servers | Nginx, Apache, Caddy, MS IIS | [web-servers.md](web-servers.md) |
| | 16 | Building For Scale | Graceful Degradation, Throttling, Backpressure, Load Shifting, Circuit Breaker, Instrumentation/Monitoring/Telemetry | [building-for-scale.md](building-for-scale.md) |
| | — | Configuration management | 12-factor config, env vars, validate at boot, ▶17 | [configuration-management.md](configuration-management.md) |
| | — | Observability | logs, metrics, tracing, ▶18 | [observability.md](observability.md) |
| | — | Graceful shutdown | SIGTERM, drain, deadline, ▶19 | [graceful-shutdown.md](graceful-shutdown.md) |
| | — | Containers & Docker | Dockerfile, layers, images, k8s | [containers-docker.md](containers-docker.md) |
| | — | Docker Compose | services, networks, volumes, `compose up`/`down` | [docker-compose.md](docker-compose.md) |
| **Parallel · optional** | 21 | Frontend Basics | HTML, CSS | [frontend-basics.md](frontend-basics.md) |
| | 23 | AI Assisted Coding | Copilot, Cursor, Claude Code, Antigravity, Prompting Techniques, Code Reviews, Documentation Generation, Refactoring | [ai-assisted-coding.md](ai-assisted-coding.md) |
| | 24 | Applications (AI features) | OpenAI, Anthropic, Gemini, RAGs, Vectors, Embeddings, Agents, Skills, MCP | [ai-applications.md](ai-applications.md) |
| | 25 | Integration Patterns (AI) | Streaming, Structured Outputs, Function Calling | [ai-integration-patterns.md](ai-integration-patterns.md) |
| | — | System design | the sibling interview track: trade-offs, components, sizing | [system-design.md](system-design.md) |

`system-design.md` is the sibling-track note: the roadmap links it as a button
to [roadmap.sh/system-design](https://roadmap.sh/system-design), so it is a
companion to the [DSA/interview track](../dsa/README.md), not a roadmap step.

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
