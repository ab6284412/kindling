# Learn about APIs
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, OpenAPI Initiative, Mozilla Contributors

## What it is

The roadmap's ninth step: the different ways a backend exposes its
functionality to other programs — **REST, GraphQL, gRPC, SOAP, JSON APIs,
and OpenAPI specs**. For a junior FastAPI dev, this section is "what does my
API actually look like from the outside."

## The concepts

- **REST** — architectural style: resources addressed by URL, manipulated
  with HTTP verbs, stateless; the default for most web APIs.
- **JSON APIs** — the wire format and the de-facto REST payload standard;
  also a specific spec (jsonapi.org) for resource serialization.
- **GraphQL** — one endpoint, client declares the exact shape of data it
  needs; query language + server runtime (nice for mobile/clients, adds a
  resolver layer).
- **gRPC** — high-performance RPC over HTTP/2, binary protobuf encoding,
  typed contracts via `.proto` files; for internal service-to-service
  calls (see `message-brokers.md` for the messaging comparison).
- **SOAP** — XML-based heavyweight RPC from the early 2000s; legacy
  enterprise interop, you mostly *consume* it.
- **Open API Specs** — machine-readable contract for REST APIs (YAML/JSON
  describing endpoints, schemas); FastAPI generates it for free via
  `/openapi.json`.

## How it works

An API is a contract: request shape → response shape. The deeper your
`http-request-response.md` understanding, the easier all of this is — REST
*is* HTTP done deliberately. OpenAPI is the tool that makes the contract
checkable by machines (clients, docs, mock servers).

## How it fails (review checklist)

- **REST that isn't** — verbs and status codes used wrong (`POST` for reads,
  200 for everything), URLs as actions not resources.
- **gRPC/GraphQL as defaults** — both add a layer and a learning curve;
  plain REST is right until you have a concrete need (internal fan-out →
  gRPC; many-shaped clients → GraphQL).
- **Docs drift** — the OpenAPI spec and the code disagree; FastAPI
  sidesteps this by deriving the spec from the code.
- **SOAP everywhere** — no.

## Build that proves it

`builds/http-server.md` builds a raw HTTP server by hand — the deep
practice for this section. The REST half: design a REST resource for one of
your models, then check it against your app's `/openapi.json`.

## Further reading
- Sriniously, "Complete REST API Design" (▶11) — https://www.youtube.com/watch?v=RG6q57DwV8Y (Feb 8, 2025)
- roadmap.sh, https://roadmap.sh/backend — "Learn about APIs" step
  (fetched Aug 3 2026)
- OpenAPI Initiative, https://spec.openapis.org/oas/latest.html — OpenAPI
  Specification (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/HTTP/Status —
  HTTP response status codes (fetched Aug 3 2026)
