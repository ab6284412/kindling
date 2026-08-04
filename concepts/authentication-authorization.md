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

No build yet. The drill: add cookie-session login to a test FastAPI app,
then add JWT auth with a short expiry + refresh, and prove a tampered token
fails signature verification.

## Further reading
- Sriniously, "Authentication and authorization" (▶8) — https://www.youtube.com/watch?v=A95rliroC8Q (Dec 23, 2024)
- roadmap.sh, https://roadmap.sh/backend — authentication cluster (fetched
  Aug 3 2026)
- Auth0, https://jwt.io/introduction — "Introduction to JSON Web Tokens"
  (fetched Aug 3 2026)
- OAuth.net, https://oauth.net/2/ — "OAuth 2.0" (fetched Aug 3 2026)
