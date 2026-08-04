# Application layers: controllers, services, repositories, middleware, request context
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

The canonical way to slice a backend's logic so it stays maintainable:
controllers handle HTTP, services hold business rules, repositories own data
access, middleware runs cross-cutting concerns, and a request context threads
shared state through one request. Sriniously's ▶10 walks all of them.

## How it works

- **Controller** (route handler): parse/validate, call a service, serialize the
  response. No business logic.
- **Service**: the business rules and use cases. Knows nothing about HTTP or SQL.
- **Repository**: the data layer — queries/CRUD behind an interface so the
  service doesn't know the DB.
- **Middleware**: runs before/after handlers for cross-cutting concerns (auth,
  logging, CORS).
- **Request context**: a per-request object (current user, request id, DB
  session) passed down instead of global state.

## How it fails

- **God controller**: business logic in route handlers — untestable, and every
  endpoint re-implements the same rule.
- **Leaky repository**: services doing raw SQL — DB change ripples everywhere.
- **Global mutable state**: a global "current user" that's actually shared
  across concurrent requests (classic Flask `g` misuse, thread races).
- **Middleware doing business work**: auth middleware enforcing *policies*, not
  just *identity*.
- No request context → threading `user_id` through every function signature.

## Build that proves it

[builds/fastapi-crud.md](../builds/fastapi-crud.md) — split router (controller) from a
service with the business rule and a repository wrapping the DB session; add a
dependency-injected request context via FastAPI's `Depends`.

## Further reading
- Sriniously, "Controllers, services, repositories, middlewares, request context" (▶10) — https://www.youtube.com/watch?v=hyc-7w3pee8 (Jan 16, 2025)