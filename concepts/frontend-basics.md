# Frontend basics (HTML, CSS, JavaScript)
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Mozilla Contributors

## What it is

The roadmap's frontend step: the minimum a backend developer must know about
the client that talks to their API — **HTML, CSS, and JavaScript**. You're
not a frontend engineer; you need to read the UI, debug the network tab,
and render a page well enough to test your API.

## The concepts

- **HTML** — the structure: elements/attributes; `<form>` and its default
  `application/x-www-form-urlencoded` POST are the *original* API client.
- **CSS** — presentation; knowing it exists and how selectors cascade is
  enough to not be lost when the page looks broken.
- **JavaScript** — the language the browser runs; you need `fetch()`
  (async HTTP), reading the console, and basic DOM access to debug your own
  backend's responses end-to-end.

## How it fails (review checklist)

- **"The frontend is magic"** — if you can't open DevTools → Network and
  read your own API's request/response, you can't debug anything.
- **Confusing client-side with server-side validation** — the browser's
  HTML5 validation is a UX nicety, not a security control; validate
  server-side (see `web-security.md`).
- **CORS misunderstandings** — "my API works in curl but the browser
  blocks it" is CORS, not your API being broken (`web-security.md`).

## Build that proves it

No build yet. The drill: hand-write a static page with a form that POSTs
to your FastAPI app and renders the JSON response via `fetch` — no
framework. That exercises HTML + JS + your API in one loop.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Frontend Basics" step
  (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/HTML —
  "HTML: HyperText Markup Language" (fetched Aug 3 2026)
