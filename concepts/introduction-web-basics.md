# Introduction: how the web works
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Mozilla Contributors

## What it is

The first step of the backend roadmap: the mental model every web developer
needs before touching a framework. Six questions, each a concept in its own
right: how does the internet work, what is HTTP, what is a domain name, what
is hosting, how does DNS work, and how do browsers work.

## The concepts

- **How does the internet work?** — a network of networks: clients and
  servers exchange messages over packet-switched links, addressed by IP.
- **What is HTTP?** — the request/response protocol browsers use to talk to
  servers; see `http-request-response.md` for the full treatment.
- **What is a domain name?** — the human-readable alias (`example.com`) that
  maps to an IP address.
- **What is hosting?** — running your app's server on a machine reachable
  from the internet (VPS, PaaS, cloud).
- **DNS and how it works?** — the distributed directory that resolves
  `example.com` → `93.184.216.34`; your browser caches the answer to avoid a
  lookup per request.
- **Browsers and how they work?** — the client: parses HTML/CSS/JS, issues
  HTTP requests, renders the page.

## How it fails (review checklist)

- **Wrong mental model:** thinking "the internet" and "HTTP" are the same —
  HTTP is one protocol riding on top of the network.
- **Skipping DNS:** a backend dev who can't explain a cache TTL vs. name
  resolution will misdiagnose "the site doesn't resolve" vs. "the server is
  down."
- **Framework-first learning:** jumping to FastAPI without this model makes
  every "why is this slow?" question unanswerable.

## Build that proves it

No build yet. Write, from memory, the sequence of events from typing
`https://example.com` in a browser to seeing the page — DNS lookup, TCP,
TLS, HTTP request, server response, rendering. That trace is the test.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Introduction" step (fetched
  Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works —
  "How the Web works" (fetched Aug 3 2026)
