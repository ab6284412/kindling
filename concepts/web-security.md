# Web security
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, OWASP, Mozilla Contributors

## What it is

The roadmap's security cluster (grouped with Building For Scale in the
current layout, but treated here as its own concept): the threats a web app
faces and the defenses you must ship by default — **HTTPS, SSL/TLS, OWASP
risk classes, CORS, server security, CSP, and the hashing algorithms** used
for passwords.

## The concepts

- **HTTPS / SSL/TLS** — encryption in transit: the browser and server agree
  on a TLS session (certificate → key exchange → symmetric encryption) so a
  middleman can't read or tamper with traffic.
- **OWASP Risks** — the top-10 taxonomy of web vulnerabilities (injection,
  broken auth, XSS, SSRF, misconfiguration, etc.); the shared vocabulary
  for "why is this dangerous?"
- **CORS** — the browser's rule for *which origins* may read your API's
  responses; misconfiguring `Access-Control-Allow-Origin` to `*` with
  credentials is how a random site exfiltrates your users' data.
- **Server security** — hardening the box: no default creds, patched, least
  privilege, only needed ports exposed.
- **CSP** — Content-Security-Policy headers restrict what scripts a page may
  run; the defense against stored/injected XSS payloads.
- **Hashing algorithms** — password storage. MD5 and SHA-1/2 are *fast*
  hashes (wrong for passwords); **bcrypt and scrypt** are slow,
  salted, deliberately expensive — the right tools for password hashing.

## How it works

Security is layered, and each layer is a *default*, not a feature you add
later: terminate TLS, validate every input at the trust boundary, store
password hashes with bcrypt/scrypt, set CORS and CSP correctly, keep the
server patched. See `authentication-authorization.md` for the auth half.

## How it fails (review checklist)

- **Passwords hashed with MD5/SHA** — trivially brute-forced and rainbow-
  table-able; a breach leaks every password.
- **HTTP in production** — session cookies and tokens travel in clear text;
  any network observer steals them.
- **CORS `*` + credentials** — a classic browser-side backdoor.
- **Injection unfixed** — parameterized queries are non-negotiable (see
  `transactions-acid.md` / ORM notes); string-concatenated SQL is a breach
  waiting to happen.
- **TLS but no CSP/validation** — encryption is the beginning, not the end.

## Build that proves it

No build yet. The drill: run a test app over HTTP, capture the plaintext
cookie with a packet capture or devtools, then enable TLS and show it's
gone — and switch a bcrypt hash of a password into your app.

## Further reading
- Sriniously, "Backend Security: Everything You Need" (▶20) — https://www.youtube.com/watch?v=xB1C1xZZW4k (Dec 14, 2025)
- roadmap.sh, https://roadmap.sh/backend — security cluster (fetched Aug 3 2026)
- OWASP, https://owasp.org/www-project-top-ten/ — "OWASP Top Ten" (fetched
  Aug 3 2026)
- OWASP, https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html —
  "Password Storage Cheat Sheet" (fetched Aug 3 2026)
