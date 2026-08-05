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

## Drill

Goal: write a validate-then-transform pipeline and prove that validating the
coerced value hides bad input.

Steps:
1. stdlib. In one `python3` session:
   ```python
   from datetime import date
   raw = {"name": "  Ada Lovelace  ", "age": "17", "joined": "2015-08-03"}
   # validate first — on the RAW strings
   assert raw["age"].isdigit(), "age must be digits"
   assert 0 <= int(raw["age"]) <= 120, "age out of range"
   joined = date.fromisoformat(raw["joined"])   # raises on bad format
   # then transform
   slug = raw["name"].strip().lower().replace(" ", "-")
   age = int(raw["age"])
   print(slug, age, type(age), joined)  # ada-lovelace 17 <class 'int'> 2015-08-03
   ```
2. Now break it: change `raw["age"]` to `"seventeen"`. The
   `assert raw["age"].isdigit()` line raises *before* any `int()` conversion —
   bad input never reaches the transform.
3. Prove the order matters: if you had coerced first (`age = int(raw["age"])`)
   and validated the result, the string `"17"` would pass silently and
   `"seventeen"` would crash with a `ValueError` — an unhandled 500 instead of
   a clean boundary rejection.

Self-check (pass/fail):
- Step 1 prints `ada-lovelace 17 <class 'int'> 2015-08-03`.
- With `"age": "seventeen"`, the script fails at the `isdigit()` assert line —
  you can name the line and why validation ran before transformation.
- You can state the order in one sentence (validate raw → transform) and how
  FastAPI/pydantic does the same at the boundary.

Why this matters: validate-then-transform at the boundary is what FastAPI does
with pydantic; skip it and bad input reaches business logic as a 500 instead of
a 422.

## Further reading
- Sriniously, "Validations and transformations" (▶9) — https://www.youtube.com/watch?v=qedj_JjjL-U (Jan 12, 2025)