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

## Further reading
- Sriniously, "Serialization and Deserialization" (▶7) — https://www.youtube.com/watch?v=vzg90tY3uM0 (Dec 11, 2024)