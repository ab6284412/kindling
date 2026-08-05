# Authentication and authorization
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Auth0 (JWT), OAuth.net

## What it is

The roadmap's authentication cluster: **who are you** (authentication) and
**what may you do** (authorization) — via **basic auth, cookie-based auth,
token auth (JWT), OAuth, OpenID Connect, and SAML**. For a junior, this is
the difference between "I can log in" and "I can log in securely."

## The concepts

- **Basic Authentication** — username:password in the `Authorization` header
  (base64, NOT encryption); fine for dev, must be over HTTPS only.
- **Cookie-based auth** — server sets an opaque `session` cookie; the
  browser sends it back; state lives server-side.
- **Token authentication (JWT)** — a signed token (header.payload.signature)
  carries identity; the server verifies the signature instead of storing
  session state. Stateless, but tokens can't be revoked by logout alone.
- **OAuth** — delegated authorization: a user grants a *third-party app*
  limited access to their account (e.g. "login with Google"); issues access
  tokens, not passwords.
- **OpenID (Connect)** — the identity layer on top of OAuth: a standard
  way to verify *who* the user is, not just *what* they authorized.
- **SAML** — the enterprise XML predecessor of OIDC (SSO in corporate
  IdPs); legacy interop.

## How it works

Auth is one of the few places "just use a library" is the *correct* answer
— rolling your own sessions/signatures is how breaches happen. Choose a
pattern by where state should live: sessions in the cookie (state
server-side), or stateless JWTs for APIs.

## How it fails (review checklist)

- **JWT secret in the codebase** — the signature is only as good as the
  key; leaked key = forge any user.
- **No token expiry/rotation** — a stolen long-lived token is a permanent
  backdoor.
- **Never revocable tokens for logout** — you need a denylist/refresh
  tokens if logout must actually log out.
- **JWTs for server-side sessions** — if you need revocation and freshness,
  an opaque session in a DB/Redis beats a self-contained token.
- **Storing passwords instead of hashes** — never; bcrypt/scrypt
  (`web-security.md`).

## Build that proves it

Proven by [builds/auth-security.md](../builds/auth-security.md). The drill: add
cookie-session login to a test FastAPI app, then add JWT auth with a short
expiry + refresh, and prove a tampered token fails signature verification.

## Drill

Goal: build a minimal JWT with stdlib `hmac` and prove the signature binds
header+payload to the secret. Stdlib only — no libraries.

Steps:
1. Save this as `jwt_drill.py`:
   ```python
   import base64, hashlib, hmac, json

   SECRET = b"hunter2"

   def b64(b):
       return base64.urlsafe_b64encode(b).rstrip(b"=")

   def make_token(payload, secret=SECRET):
       header = b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
       body = b64(json.dumps(payload).encode())
       sig = b64(hmac.new(secret, header + b"." + body, hashlib.sha256).digest())
       return header + b"." + body + b"." + sig

   def verify(token, secret=SECRET):
       header, body, sig = token.split(b".")
       good = hmac.new(secret, header + b"." + body, hashlib.sha256).digest()
       return hmac.compare_digest(sig, b64(good))

   tok = make_token({"user": "alice", "exp": 9999999999})
   print("valid:", verify(tok))
   print("tampered:", verify(tok[:-3] + b"AAA"))          # flip signature
   forged = make_token({"user": "bob"}, secret=b"leaked-key")
   print("forged w/ wrong secret:", verify(forged))       # fails under real key
   ```
2. Run `python3 jwt_drill.py`.
3. Swap `SECRET` to a different value and re-run — every old token now fails.

Self-check (pass/fail — run it alone): `valid` prints `True`, `tampered`
prints `False` (a one-byte change breaks the signature), and re-running with a
different `SECRET` makes the old token fail. That last one is the lesson: the
signature is only as strong as the key — a leaked `SECRET` lets anyone forge
any user.

Why this matters: JWTs are only trusted because of this signature; keep the
secret out of the repo, add expiries, and remember a valid signature proves
*who signed it*, not that the user still exists.

## Further reading
- Sriniously, "Authentication and authorization" (▶8) — https://www.youtube.com/watch?v=A95rliroC8Q (Dec 23, 2024)
- roadmap.sh, https://roadmap.sh/backend — authentication cluster (fetched
  Aug 3 2026)
- Auth0, https://jwt.io/introduction — "Introduction to JSON Web Tokens"
  (fetched Aug 3 2026)
- OAuth.net, https://oauth.net/2/ — "OAuth 2.0" (fetched Aug 3 2026)
