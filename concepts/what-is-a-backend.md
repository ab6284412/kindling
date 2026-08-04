# What is a backend
Created 2026-08-04 · Last verified 2026-08-04
Provenance: AI-drafted · Credits: Sriniously (@sriniously)

## What it is

The backend is the part of a system that runs on servers, out of the user's
browser: it holds state, enforces rules, and speaks to databases and third
parties. The frontend asks; the backend decides and answers. Sriniously's ▶3
is the tour: what a backend is, how backends work, and why they exist at all.

## How it works

- The backend owns the data and the business rules; the frontend is a remote
  controller for it.
- It exposes an interface (usually HTTP) so any client — browser, phone, other
  service — can interact without knowing the internals.
- Behind the interface: routing, validation, business logic, storage, and
  security. The rest of this workspace's stages are those layers in depth.

## How it fails

- Backend as "the API folder" — a backend is a full system (data, jobs,
  security), not a CRUD endpoint list.
- Trusting the client: every request crosses a trust boundary, so the backend
  re-validates and re-authorizes everything.
- No clear boundary: mixing view concerns, business rules, and storage access
  into one function is how monoliths rot.

## Build that proves it

Build: [builds/http-server.md](../builds/http-server.md) — write the request/response
core by hand so the boundary is concrete, not assumed.

## Further reading
- Sriniously, "What is a Backend, how they work and why" (▶3) — https://www.youtube.com/watch?v=6Ss4dJD9Kzg (Sep 24, 2024)
