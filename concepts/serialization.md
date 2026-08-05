# Serialization and deserialization
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

Serialization turns in-memory objects into a byte/format stream you can send
or store; deserialization turns that stream back into objects. It's the
shape-shifting at every API boundary. Sriniously's ▶7 is the dedicated video.

## How it works

- Serialize: object → text (commonly JSON) with a schema, so any language can
  read it. Deserialize: text → object, validating types along the way.
- Schema is the contract: field names, types, nullability, nesting. That's what
  OpenAPI/serializers derive from.
- Frameworks (FastAPI's `pydantic`) do this declaratively: declare the shape,
  get parse + validate + re-serialize for free.

## How it fails

- **Drift**: the API emits `created_at` on write but you read `timestamp` on
  the way back — schema mismatch.
- **Silent type coercion**: string `"5"` becoming int `5` when you didn't ask,
  hiding bad data.
- **Infinite/NaN issues**: Python's `NaN`/`Infinity` don't survive JSON; circles
  in objects blow up recursion.
- **Over-fetching / leaking fields**: serializing the whole ORM model leaks
  password hashes. Serialize a DTO, not the entity.

## Build hook

[builds/fastapi-crud.md](../builds/fastapi-crud.md) — pydantic request/response models
are exactly serialization as schema.

## Drill

Goal: round-trip data through stdlib `json` and see silent coercion, NaN, and
field-leaking for yourself.

Steps:
1. stdlib. In one `python3` session:
   ```python
   import json
   payload = {"id": 5, "name": "widget", "price": "5.0"}
   wire = json.dumps(payload)
   back = json.loads(wire)
   print(wire)                             # {"id": 5, "name": "widget", "price": "5.0"}
   print(back["id"], type(back["price"]))  # 5 <class 'str'>
   ```
   `price` comes back as a string — JSON carries types exactly; nothing was
   silently coerced. Any "5 → 5" you've seen was your serializer (pydantic)
   doing it, not the wire.
2. NaN: `print(json.dumps({"x": float("nan")}), json.dumps({"x": float("inf")}))`
   — prints `NaN` and `Infinity`, which are *not* valid JSON per RFC 8259; a
   strict consumer rejects the payload.
3. Leaking fields: `u = {"username": "alice", "password_hash": "abc123"}`;
   print `json.dumps(u)` (serialize the whole entity — the hash is on the
   wire), then print `json.dumps({k: u[k] for k in ("username",)})` (an
   explicit DTO — the hash is gone).

Self-check (pass/fail):
- Step 1 prints `5` and `<class 'str'>` — you can state what the wire preserved
  vs what a serializer would have coerced.
- Step 2 prints `NaN` and `Infinity` (non-standard tokens).
- Step 3's full-entity dump contains `password_hash`; the DTO dump does not.

Why this matters: drift, silent coercion, NaN, and field leaks are the four
named serialization failures — all visible in five lines of `json`.

## Further reading
- Sriniously, "Serialization and Deserialization" (▶7) — https://www.youtube.com/watch?v=vzg90tY3uM0 (Dec 11, 2024)