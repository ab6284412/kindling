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

## Drill

Goal: prove an HTML `<form>` is an API client — it POSTs
`application/x-www-form-urlencoded` on submit — and `fetch()` is the JSON
one, using stdlib `http.server` and a browser (the only external tool).

Steps:
1. From a scratch dir, save `index.html`:
   ```html
   <form method="post" action="/submit">
     <input name="name" value="ann">
     <input name="msg" value="hello">
     <button>Send</button>
   </form>
   ```
2. Save this as `server.py` and run `python3 server.py`:
   ```python
   from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
   class H(BaseHTTPRequestHandler):
       def do_GET(self):
           self.send_response(200); self.end_headers()
           self.wfile.write(open("index.html", "rb").read())
       def do_POST(self):
           n = int(self.headers.get("Content-Length", 0))
           print(f"[server] {self.headers.get('Content-Type')}: "
                 f"{self.rfile.read(n).decode()}", flush=True)
           self.send_response(200); self.end_headers()
       def log_message(self, *a): pass
   ThreadingHTTPServer(("127.0.0.1", 8121), H).serve_forever()
   ```
3. Open `http://127.0.0.1:8121/` in a browser and click Send.
4. Add to the page body, then reload and Send again:
   ```html
   <button onclick="fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'ann'})})">Fetch</button>
   ```

Self-check (pass/fail — run it alone):
- The server prints a line starting `[server] application/x-www-form-urlencoded:
  name=ann&msg=hello` — the form's default encoding, no JS involved.
- After step 4 it also prints `application/json: {"name": "ann"}` — same
  endpoint, two encodings, and curl would show the identical urlencoded body
  the browser sent.

Why this matters: every backend dev debugs a "works in curl, breaks in the
browser" bug at some point — knowing what the browser actually sends is how
you read the Network tab instead of guessing.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Frontend Basics" step
  (fetched Aug 3 2026)
- Mozilla Contributors, https://developer.mozilla.org/en-US/docs/Web/HTML —
  "HTML: HyperText Markup Language" (fetched Aug 3 2026)
