# Build: authentication & authorization on the CRUD API
Source: [concepts/authentication-authorization.md](../concepts/authentication-authorization.md), [concepts/web-security.md](../concepts/web-security.md),
and Sriniously's playlist videos ▶8 (Authentication and authorization) and
▶20 (Backend Security)
Provenance: AI-drafted · Credits: Sriniously (@sriniously), OWASP

Goal: extend the stage-3 CRUD API with hand-built authentication and
authorization — password hashing, token login, ownership checks, and a passing
OWASP review — using only the Python stdlib, so every security decision is
visible.

## Spec

Extend [builds/fastapi-crud.md](fastapi-crud.md)'s `app.py` so that:

1. Adds a `users` table: `id`, `email UNIQUE NOT NULL`, `password_hash NOT
   NULL`, `created_at`. Adds `owner_id` to `todos` (FK → users.id).
2. `POST /register` — validates that email looks like an email, hashes the
   password with `hashlib.pbkdf2_hmac('sha256', password, salt, 210_000)`
   (per-user random salt via `os.urandom`), stores salt+hash, returns `201`
   with the user row **excluding** `password_hash` and `salt`. Duplicate email →
   `409`.
3. `POST /login` — on valid creds, creates a session: `secrets.token_hex(32)`
   stored in a `sessions(token, user_id, expires_at)` table (expiry = e.g.
   now + 7 days). Returns `{ "token": ..., "expires_at": ... }`. Wrong
   email/password → uniform `401` (no user-enumeration hint).
4. A dependency `get_current_user(token)` that reads `Authorization: Bearer
   <token>`, looks up the session, rejects with `401` if missing/invalid/
   expired. Every protected route takes it.
5. `GET /me` → the authenticated user's row.
6. Todo ownership: only the owner may `GET/PATCH/DELETE /todos/{id}`. Authenticated
   non-owner → `403`. Unauthenticated CRUD → `401`.
7. Password comparison uses `hmac.compare_digest` (constant-ish time). The app
   never logs `password`, `salt`, `password_hash`, or raw tokens.

Passes an OWASP pass/fail review:
- No SQL injection (every query parameterized),
- No mass assignment (Pydantic models allow only `email`/`password`),
- No `password_hash`/`salt`/`token` in any response,
- Every protected route actually depends on `get_current_user`.

## Constraints

- Stdlib + FastAPI + pydantic only. No `passlib`, no `jose`, no `python-jose`,
  no OAuth/token libraries.
- Hashing via `hashlib.pbkdf2_hmac` + `secrets`; session token is an opaque,
  DB-backed id — **not** a self-contained JWT (JWT is an extension).
- Build on the stage-3 `app.py` (which has no auth yet); the diff should be
  only the new tables, endpoints, and the `get_current_user` dependency.

## Self-check (pass/fail)

Run `uvicorn app:app`, then every line must behave as shown (bodies never
contain `password_hash`, `salt`, or the raw token in a non-token field):

```bash
curl -i -X POST localhost:8000/register -H 'content-type: application/json' \
  -d '{"email":"a@x.io","password":"hunter2ok"}'     # 201, no password_hash
curl -i -X POST localhost:8000/register -H 'content-type: application/json' \
  -d '{"email":"a@x.io","password":"other"}'          # 409
curl -i -X POST localhost:8000/login -H 'content-type: application/json' \
  -d '{"email":"a@x.io","password":"wrong"}'          # 401
curl -s -X POST localhost:8000/login -H 'content-type: application/json' \
  -d '{"email":"a@x.io","password":"hunter2ok"}'      # 200 {token, expires_at}
curl -i localhost:8000/todos                          # 401 (no token)
curl -i localhost:8000/me -H "Authorization: Bearer $TOKEN"   # 200, email a@x.io
```

Then: register two users **b@x.io** and **c@x.io**. As B, `POST /todos`. As C,
`GET/PATCH/DELETE /todos/{that_id}` → `403`. As B → `200`. Restart uvicorn:
the session token must now be invalid → `401` on `/me`. Sessions live in a
`sessions` table that a fresh boot wipes, so restart revocation is the point —
a *persistent* session store would keep tokens valid across restart (that is
the extension, not the baseline).

## Extensions (only after v1 passes)

- Stateless JWT (signature via `hmac` + payload) instead of DB sessions; note
  the trade-off (no revocation without a denylist).
- Login rate limiting / account lockout counters.
- Refresh token paired with a short-lived access token (▶20).
- 2FA.

## Why this matters

Most junior-work API breaches come from missing ownership checks and weak
password handling, not exotic exploits. Building auth with the stdlib makes
the mechanics — hashing, session vs stateless, authN vs authZ — concrete, and
that's what an interviewer or a security review probes.