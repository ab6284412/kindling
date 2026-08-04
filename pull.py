#!/usr/bin/env python3
"""Tech research news pull. Prints a dated digest skeleton. Stdlib only, no deps.

Usage:
    python3 pull.py                          # HN + Lobsters + Anthropic (+ OpenAI re-test)
    python3 pull.py > notes/$(date +%F)-digest.md   # seed a daily digest
    python3 pull.py search "qwen"            # HN Algolia fallback for blocked sites
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from html import unescape

UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}
BLOCKED = {
    "reddit.com": "403 bot protection; mirror on HN/Lobsters within hours",
    "producthunt.com": "403 even with cookies; mirror on HN/Lobsters",
    "theregister.co.uk": "403 on HTML/atom/headlines.json",
}
MAXHITS = 25


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def try_fetch(url: str):
    try:
        return fetch(url)
    except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        return None


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", s))).strip()


def hn(html: str):
    titles = [
        strip_tags(t)
        for t in re.findall(r'<span class="titleline"><a[^>]*>(.*?)</a>', html)
    ]
    scores = [
        int(s) for s in re.findall(r'<span class="score"[^>]*>(\d+)\s*p', html)
    ]
    return list(zip(titles, scores))[:MAXHITS]


def lobsters(html: str):
    titles = [
        strip_tags(t)
        for t in re.findall(r'<a class="u-url"[^>]*>(.*?)</a>', html)
    ]
    return titles[:MAXHITS]


def anthropic(html: str):
    cards = [
        strip_tags(c)
        for c in re.findall(r'<a href="/news/[^"]*"[^>]*>(.*?)</a>', html)
    ]
    return [c for c in cards if c][:MAXHITS]


def hn_search(query: str):
    url = (
        "https://hn.algolia.com/api/v1/search?query="
        + urllib.parse.quote(query)
        + "&restrictSearchableAttributes=title&tags=story&hitsPerPage=10"
    )
    try:
        hits = json.loads(fetch(url))["hits"]
    except (ValueError, KeyError, urllib.error.HTTPError):
        return ["(algolia fetch failed)"]
    return [
        f"- {h['title']} ({h['points']} pts, {h.get('created_at', '')[:10]})"
        + (f" {h.get('url') or ''}" if h.get("url") else " (ask)")
        for h in hits
    ]


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        for line in hn_search(" ".join(sys.argv[2:])):
            print(line)
        return 0

    today = date.today().isoformat()
    print(f"# News digest — {today}")
    print()

    for name, url, parser in (
        ("Hacker News (front page)", "https://news.ycombinator.com/", hn),
        ("Lobsters", "https://lobste.rs/", lobsters),
        ("Anthropic (anthropic.com/news)", "https://www.anthropic.com/news", anthropic),
    ):
        print(f"## {name}")
        html = try_fetch(url)
        if html is None:
            print("- fetch failed (network / bot protection) — check manually")
        else:
            for item in parser(html):
                if isinstance(item, tuple):
                    title, score = item
                    print(f"- {title} ({score} pts)" if score else f"- {title}")
                else:
                    print(f"- {item}")
        print()

    print("## Blocked / needs verification")
    # OpenAI flip-flops per AGENTS.md runbook: re-test each pull.
    openai = try_fetch("https://openai.com/news")
    if openai is not None and ("openai.com/news" not in openai and "News" not in openai[:2000]):
        print("- openai.com/news: reachable again? verify and update followups.md")
    else:
        print("- openai.com/news: JS shell / bot challenge (blocked) — mirror on HN/Lobsters")
    for name, why in BLOCKED.items():
        print(f"- {name}: {why}")
    print()
    print("## Fallback")
    print("- Search HN for the blocked topic: `python3 pull.py search \"topic\"`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
