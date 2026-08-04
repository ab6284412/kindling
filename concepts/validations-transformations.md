# Validations and transformations
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

Validation checks that incoming data *is what you expect* (right type, range,
required-ness); transformation reshapes it into the form the rest of the system
needs (string → enum, `YYYY-MM-DD` → date, display name → slug). Sriniously's ▶9
covers both as part of the request lifecycle.

## How it works

- **Validate early**: parse + validate at the API boundary (schema layer), so
  business logic can assume clean input. Fail fast with a 422/400, not a 500.
- **Transform as a step**: after validation, map the wire format to the domain
  format. Keeps "what the client sends" decoupled from "what the code wants".
- Frameworks make this declarative: FastAPI's pydantic `Field(min_length=…)`,
  type coercion, and `validator` decorators run before your handler body.

## How it fails

- **Validating too late**: business code re-checking everything, or worse,
  trusting raw input (SQL injection, path traversal start here).
- **Validation vs transformation conflated**: coercing "5" → 5 silently hides
  that the client sent a string. Validate the type, then transform explicitly.
- **Error shape inconsistency**: each handler returns a different error format
  — clients can't parse failures programmatically.
- **Half-validated updates**: `PATCH` accepts partial data but you validate the
  full entity, so legitimately partial updates 422.

## Build that proves it

[builds/fastapi-crud.md](../builds/fastapi-crud.md) — declare pydantic models with constraints,
return a consistent error body, and see validation run before your handler.

## Further reading
- Sriniously, "Validations and transformations" (▶9) — https://www.youtube.com/watch?v=qedj_JjjL-U (Jan 12, 2025)