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

## Drill

Goal: split one use case into controller/service/repository and thread a
request context through it — no globals.

Steps:
1. stdlib. Save `layers.py`:
   ```python
   from dataclasses import dataclass
   @dataclass
   class Request:
       user_id: str
       request_id: str
   store = []                     # fake "database"
   def repo_save_order(req, total):            # repository: owns data access
       store.append({"user_id": req.user_id,
                     "request_id": req.request_id, "total": total})
       return len(store) - 1
   def service_checkout(req, cart):            # service: owns business rule
       if not cart:
           return {"error": "cart empty"}
       return {"order_id": repo_save_order(req, sum(cart))}
   def controller(req, cart):                  # controller: glue only
       return service_checkout(req, cart)
   print(controller(Request("alice", "r1"), [10, 20]))   # {'order_id': 0}
   print(controller(Request("bob", "r2"), []))            # {'error': 'cart empty'}
   print(store)
   ```
2. Run it: alice's order lands in `store` with her `request_id`; bob's empty
   cart returns the error *from the service* and writes nothing.
3. Prove the repository is the only layer that knows the "DB": rewrite
   `repo_save_order` to write into a `dict` keyed by order id — controller and
   service change by zero lines.

Self-check (pass/fail):
- `store` holds exactly one row: `user_id='alice'`, `request_id='r1'` — the
  request context traveled down without a global.
- Empty cart → `{'error': 'cart empty'}`, and you can name which layer owns
  that rule (service, not controller).
- Swapping the repository's storage (list → dict) touches no other layer.

Why this matters: god controllers and global "current user" are the named
failure modes; a 20-line layering shows both fixes before they bite in FastAPI.

## Further reading
- Sriniously, "Controllers, services, repositories, middlewares, request context" (▶10) — https://www.youtube.com/watch?v=hyc-7w3pee8 (Jan 16, 2025)