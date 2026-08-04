# Fixtures

Live HTML snapshots saved on Aug 3, 2026 (PST). `tests/test_pull.py` runs the
parsers against these so pull.py stays regression-safe offline — when a site
changes its markup, the test fails before the digest comes back empty.

| Fixture | Source | What it guards |
|---|---|---|
| `hackernews.html` | `news.ycombinator.com` front page (itemlist table only) | `hn()` title/score parsing |
| `lobsters.html` | `lobste.rs` (stories `<ol>` only) | `lobsters()` `u-url` parsing |
| `anthropic.html` | `anthropic.com/news` (news-card region) | `anthropic()` card parsing |

Regenerate a fixture when its site's markup changes and you've confirmed the
new shape by hand:

```bash
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  https://news.ycombinator.com/ > /tmp/hn.html
# then slice the relevant region, mirroring the original trim
```
