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

## Drill

Goal: resolve a domain to an IP and watch HTTP run on top of TCP to see the
network layers working.

Steps:
1. stdlib: `python3 -c "import socket; print(socket.gethostbyname('example.com'))"`
   — prints an IPv4 like `93.184.216.34`. A domain name is just an alias for
   that IP; DNS did the lookup.
2. In a scratch dir run `python3 -m http.server 8126`; in another terminal
   `curl -v http://localhost:8126/ 2>&1 | grep '^[<>]'`. You see the request
   line (`GET / HTTP/1.1` — curl negotiates HTTP/1.1) and the status line
   (`HTTP/1.0 200` — SimpleHTTPRequestHandler answers 1.0); they differ because
   the client offers the newest protocol it knows while the server replies with
   the oldest it supports. Either way it's HTTP riding on TCP port 8126.
3. Make name resolution visible: `curl -v http://localhost:8126/ 2>&1 | grep -i '^> Host'`
   prints `Host: localhost:8126` — a hostname, not an IP, travels in the
   request, and the OS resolved `localhost` → `127.0.0.1` before connecting.

Self-check (pass/fail):
- `gethostbyname` prints a valid IPv4 (4 dotted octets).
- The `curl -v` output contains both `GET / HTTP/1.1` (request line) and
  `HTTP/1.0 200` (status line) — you can point at each, and explain why they
  differ (curl offers HTTP/1.1; Python's SimpleHTTPRequestHandler answers
  HTTP/1.0).
- The `Host:` grep shows a hostname, and you can list the layers at play (name
  resolution, IP, port, HTTP) and say where DNS normally sits in that chain.

Why this matters: "DNS problem vs server down" is a real junior misdiagnosis;
if you can trace which layer failed, you can point at the right one.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Introduction" step (fetched
  Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works —
  "How the Web works" (fetched Aug 3 2026)
