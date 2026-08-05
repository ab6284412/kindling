# Tech Research & Learning Lab

This folder is a research and learning workspace. Its purpose is to research the
latest news and developments in AI, developer tools, and software engineering
(e.g. OpenAI research, the Bun rewrite, new frameworks, MCP servers) and to
distill them into notes that build real understanding.

## How agents should act in this environment

### Mindset
- **We learn, not just summarize.** For every piece of research, extract a
  transferable lesson (a principle, a failure class, a skill) in addition to the
  factual summary.
- **Separate marketing from substance.** AI companies cherry-pick numbers
  (e.g. "$2,000 for ten proofs" excludes the harness, failed attempts, and
  salaries). When a claim looks too clean, ask: what is the denominator? What
  is being hidden? State both the claim and the caveat.
- **Sources first.** Always fetch the primary source (repo, paper, official
  blog) before secondary commentary. Cite the URL and the publish date.
- **Stay current.** Today's date is 2026. Prefer the latest information; flag
  when a search result is older or superseded.

### Trusted sources

Where news breaks early and regularly, grouped by category. Use these as
starting points; always verify against the primary source before treating
something as fact.

**Tech news (early / high signal)**
- Hacker News — news.ycombinator.com — the best general index of tech/dev news; strong discussion. Note the *date* and points: high points + comments = discussed, not necessarily true.
- Lobsters — lobste.rs — invite-only dev news; higher signal, slower.
- Reddit: r/programming, r/technology, r/saas, r/startups, r/selfhosted.
- The Register — theregister.co.uk — fast dev/ops news, good for breakages/security.
- Ars Technica / The Verge — depth and analysis on mainstream tech.

**AI / dev-tools specific**
- Official blogs (primary): openai.com/news, anthropic.com/news, blogs on GitHub, bun.com/blog, ziglang.org.
- Simon Willison's blog — simonwillison.net — the highest-trust individual commentary on AI news; checks the claims himself.
- Changelog — changelog.com — open source / dev tool releases and podcasts.
- dev.to — community posts; treat as opinion, check the code yourself.
- Hacker News + Lobsters again — AI papers and model releases usually surface here within hours.
- The Sequence / Latent Space / Import AI — AI newsletters that summarize the week; good for catching up, cite the underlying source.

**SaaS / startups / indie / product**
- Indie Hackers — indiehackers.com — indie SaaS, bootstrapped startups, revenue stories.
- Product Hunt — producthunt.com — product launches. Good for *what launched*, not for depth.
- Starter Story — starterstory.com — how small startups started (real numbers).
- SaaStr — saastr.com — SaaS sales/marketing/growth wisdom.
- Lenny's Newsletter — lennysnewsletter.com — product + growth, high signal.
- Failory — failory.com — startup post-mortems (learn from what broke).
- 37signals blog (Signal v. Noise) — SaaS philosophy and "small, simple" engineering (fits the Ponytail mindset).
- Funding: TechCrunch, Crunchbase News, PitchBook, Dealroom — for who raised what; treat round sizes as often approximate.

**Tiers of trust (how to weight these)**
1. **Primary source** — official blog, repo, paper, release notes. Highest trust; cite this.
2. **High-signal commentary** — Hacker News/Lobsters discussions, Simon Willison. Great for context and caveats, still verify numbers.
3. **Aggregators & launches** — Product Hunt, newsletters, funding roundups. Useful for *discovery*; never cite as the source of record.
4. **X/Twitter** — earliest but unverified. Use only to *find* what just broke, then go fetch the primary source. Do not trust screenshots or thread claims.

When in doubt: fetch the official source and check the date before you write it down.

### News pull runbook (provenance: tested Aug 3, 2026 — re-test per followups.md)

How to actually pull the latest headlines from this machine. Learned from the
first real pull: some sources need a specific parse, and some are hard-blocked.

**Automation:** `python3 pull.py` in this folder implements the runbook — HN,
Lobsters, Anthropic, the Algolia fallback (`python3 pull.py search "topic"`),
and the blocked-source notes. Run it to seed a digest, then verify before
citing. `python3 pull.py > notes/$(date +%F)-news-digest.md`.
`python3 pull.py digest` auto-summarizes the headlines with a local Ollama
nano model (`llama3.2:1b`) and writes `notes/<date>-news-digest.md` with
`## Further reading` URLs from the parsed links (Ollama must be running; if it
isn't, the digest falls back to raw headlines and marks itself un-summarized).
Only fetch manually when pull.py gives something unexpected. If a parser
returns nothing, first run `python3 -m unittest discover -s tests` — a markup
change at the source will fail a fixture test before it silently empties a
digest.

**Working (direct fetch + parse)**
- Hacker News — fetch `news.ycombinator.com` front page HTML; story titles come
  with `(points, comments)`. Reliable.
- Lobsters — fetch `lobste.rs`; parse story titles from HTML. Works.
- OpenAI — **now serves a JS shell** (Cloudflare bot challenge, ~10KB page,
  no `/news/*` links). Treat as blocked; fall back to HN/Lobsters mirrors.
  Re-test before assuming it's back.
- Anthropic — fetch `anthropic.com/news`; parse the `<a href="/news/...">…</a>`
  cards and strip tags — each card is `Category | Date | Title | blurb`.
  Do **not** look for `<h2>` or `__NEXT_DATA__` — Anthropic ships neither.
- Changelog — fetch `changelog.com`; items live at `/news/<id>` anchors.
  As of Aug 3 2026 the homepage only surfaces through `#185` (Apr 2026) —
  weekly news appears paused/reorged; verify before citing it as current.
- Indie Hackers — fetch `indiehackers.com`; titles only, content is mixed.

**Blocked (403 bot protection — retry once, then skip)**
- Reddit (`r/*.json`, `.rss`, browser UA all blocked), Product Hunt (blocked
  even with cookies), The Register (HTML, `.atom`, and `headlines.json` all 403).
- Fallback: these stories are mirrored on Hacker News / Lobsters within hours.
  Search HN Algolia (`hn.algolia.com/api/v1/search`) for the same topic instead.

**Parsing gotchas**
- RSS/Atom namespaces: use `root.iter()` and match `tag.endswith('entry')` /
  `'item'`. A plain `.findall('entry')` silently returns nothing on namespaced feeds.
- Don't assume Next.js sites ship `__NEXT_DATA__` (Anthropic does not).
- A browser UA in curl beats Python `urllib`, but neither beats 403 bot protection.

### Workflow
1. Research the topic using web search and web fetch. Prefer primary sources.
2. Summarize: what it is, what happened, key numbers, key actors, date.
   Credit the article's author by name in the note.
3. Extract lessons: what transfers to a junior backend (FastAPI/Python) engineer?
   What failure classes or review checklist items does it reveal?
4. Add your own take: skepticism, implications, what to watch next.
5. Mark provenance on the note (`AI-drafted` or `Human-written`).
6. Save the artifact per its convention (digest/knowledge/concept/build/drill),
   keeping it concise and scannable.
7. If the item signals a trend, add a falsifiable row to `news-ledger.md`.

### Interaction with the user
- The user is a junior backend (FastAPI/Python) developer. Tailor explanations
  and examples to that context.
- When asked "what should I learn from this", give a specific, actionable take —
  a skill, a checklist item, or a drill — not a generic "stay curious".
- Offer to go deeper: read the HN discussion thread, dig into the primary
  source, or turn a lesson into a practice exercise.

### Notes convention
- Dated daily digests live in `notes/` (`notes/<date>-news-digest.md`) and *rot*.
  Don't re-summarize a topic that already has a knowledge note; link it.
- Interview-prep areas live in `dsa/` (patterns-first notes, roadmap-ordered
  by its README, puzzles at `dsa/puzzles/`), `soft-skills/` (communication
  skills at `soft-skills/communication-skills/`, jargon one term per file
  under `soft-skills/communication-skills/jargon/`). Same provenance rules.
- Evergreen lessons live in `knowledge/<topic-slug>.md`. Structure each:
  - `# <Topic>` + `Created <date> · Last verified <date>`
  - `## Summary` (what happened, who, when, key numbers)
  - `## Lesson` (transferable takeaway)
  - optional `## Drill` / `## Open questions`
  - `## Further reading` (URLs with dates) — fetch and confirm every URL; a note
    without a source is a rumor.
  - The index `knowledge/README.md` maps each note → drill → learning.md
    stage. Update it when you add a note; a stale `Last verified` is the
    freshness alarm.
- Keep notes tight. Prefer bullets over prose. Code examples only when they
  illustrate a lesson.
- **Provenance & credits (required on every content file):** a `Provenance:` line
  (`AI-drafted` or `Human-written`) and a `Credits:` line naming the human
  author(s) of the sources. AI makes mistakes — an AI-drafted note's claims are
  only as good as its `## Further reading`. Credit every article's author by name;
  summarizing someone's post without naming them is misattribution.
- The systematic textbook lives in `concepts/<concept>.md` (one article per
  concept, traceable to sources), indexed by stage in `concepts/README.md`.
- Hand-made full-concept exercises live in `builds/<thing>.md`; short
  lesson-specific reps live as a `## Drill` section embedded in the concept or
  knowledge note they practice.
- `news-ledger.md` is the news ledger: every digest item that signals a
  trend gets one falsifiable row there; rows get scored (held/fizzled/partial)
  against evidence on review.
- When a lesson can be practiced, write a `## Drill` section in the owning
  note: goal, steps, and a self-check the learner can run alone. A knowledge
  note without a drill is a summary; with one it's a skill.
- `learning.md` is the structured fundamentals curriculum (freeCodeCamp-style,
  free project-based sites) for a junior FastAPI/Python backend. Drills are the
  short lesson-specific reps (embedded in concepts); the path stages are the
  deep practice. Point
  learners to the matching stage when a news lesson touches a fundamental.
- `followups.md` is the standing-issues tracker. Every digest session: re-test
  anything listed, update its status, and add new open questions there instead
  of burying them in a dated note.
- `templates/` has skeletons for knowledge notes, drills, and digests — use
  them for new artifacts. `CONTRIBUTING.md` encodes the same rules for outside
  contributors. `README.md` + `LICENSE` make the workspace publishable.
- Dates like "tested Aug 3 2026" in this file are **provenance**, not truth —
  they record when a claim was checked. Re-test before treating them as current
  (see `followups.md`).

### Guardrails
- Do not invent URLs or quotes. Only include facts found in fetched sources.
- Do not write code files in this folder unless the user asks to prototype
  something related to the research.
- If a topic needs deep reading, offer a focused deep-dive instead of skimming
  a dozen pages shallowly.
