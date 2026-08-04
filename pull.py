#!/usr/bin/env python3
"""Tech research news pull. Prints a dated digest skeleton. Stdlib only, no deps.

Usage:
    python3 pull.py                          # HN + Lobsters + Anthropic (+ OpenAI re-test)
    python3 pull.py > notes/$(date +%F)-digest.md   # seed a daily digest
    python3 pull.py digest                   # auto-summarize w/ local Ollama nano model
                                             #   -> notes/<date>-news-digest.md (needs ollama running)
    python3 pull.py search "qwen"            # HN Algolia fallback for blocked sites
"""
from __future__ import annotations

import json
import os
import re
import subprocess
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
    pairs = re.findall(
        r'<span class="titleline"><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html
    )
    scores = [
        int(s) for s in re.findall(r'<span class="score"[^>]*>(\d+)\s*p', html)
    ]
    items = [
        (strip_tags(t), u, scores[i] if i < len(scores) else 0)
        for i, (u, t) in enumerate(pairs)
    ]
    return items[:MAXHITS]


def lobsters(html: str):
    pairs = re.findall(
        r'<a class="u-url"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html
    )
    return [(strip_tags(t), u, 0) for u, t in pairs][:MAXHITS]


def anthropic(html: str):
    pairs = re.findall(r'<a href="(/news/[^"]*)"[^>]*>(.*?)</a>', html, re.S)
    items = []
    for u, body in pairs:
        head = re.search(
            r"<h[1-4][^>]*class=\"[^\"]*title[^\"]*\"[^>]*>(.*?)</h[1-4]>", body, re.S
        ) or re.search(r"<h[1-4][^>]*>(.*?)</h[1-4]>", body, re.S)
        title = strip_tags(head.group(1)) if head else strip_tags(body)
        if title:
            items.append((title, "https://www.anthropic.com" + u, 0))
    return items[:MAXHITS]


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


SOURCES = (
    ("Hacker News (front page)", "https://news.ycombinator.com/", hn),
    ("Lobsters", "https://lobste.rs/", lobsters),
    ("Anthropic (anthropic.com/news)", "https://www.anthropic.com/news", anthropic),
)


def collect():
    """Fetch all sources; return {name: [(title, url, score), ...], 'failed': [...]}."""
    out = {}
    failed = []
    for name, url, parser in SOURCES:
        html = try_fetch(url)
        if html is None:
            failed.append(name)
            out[name] = []
        else:
            out[name] = parser(html)
    out["failed"] = failed
    return out


ANSI = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")


def summarize_headlines(titles: list[str], model: str = "llama3.2:1b") -> str:
    """Pipe titles into a local Ollama model; return its digest skeleton."""
    prompt = (
        "Group these tech-news headlines into sections by topic (one headline "
        "per bullet, keep the title). Use markdown headers. Max 12 words per "
        "bullet.\n\n" + "\n".join(f"- {t}" for t in titles)
    )
    try:
        proc = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return f"## Summary\n- summarizer unavailable: {e}"
    if proc.returncode != 0:
        return "## Summary\n- summarizer unavailable: " + proc.stderr.strip()
    return ANSI.sub("", proc.stdout.strip())


def write_digest(data: dict, model: str = "llama3.2:1b", summarize=None) -> str:
    """Summarize collected headlines with a local nano model and write the note."""
    summarize = summarize or summarize_headlines
    today = date.today()
    notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes")
    os.makedirs(notes_dir, exist_ok=True)
    path = os.path.join(notes_dir, f"{today.isoformat()}-news-digest.md")

    titles = [
        f"[{item[0]}] {name}"
        for name in ("Hacker News (front page)", "Lobsters", "Anthropic (anthropic.com/news)")
        for item in data[name]
    ]
    summary = summarize(titles, model)
    unsummarized = "summarizer unavailable" in summary

    lines = [
        f"# News digest — {today.strftime('%b %-d, %Y')}",
        "",
        "Provenance: AI-drafted (nano local model, headlines only) — verify before citing.",
        "",
        "## Summary",
    ]
    lines.append(summary if summary.startswith("##") else summary)
    if unsummarized:
        lines.append(
            "- (raw headlines below; Ollama not reachable — start it with `ollama serve`)"
        )
        for name in ("Hacker News (front page)", "Lobsters", "Anthropic (anthropic.com/news)"):
            lines.append("")
            lines.append(f"### {name}")
            for title, _, score in data[name]:
                lines.append(f"- {title}" + (f" ({score} pts)" if score else ""))
    lines += [
        "",
        "## Further reading",
    ]
    seen = set()
    for name in ("Hacker News (front page)", "Lobsters", "Anthropic (anthropic.com/news)"):
        for title, url, _ in data[name]:
            if url in seen or not url:
                continue
            seen.add(url)
            lines.append(f"- {title} — {url} ({today.strftime('%b %-d, %Y')})")
    lines += [
        "",
        "## Open questions",
        "- (none yet)",
        "",
    ]
    text = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        for line in hn_search(" ".join(sys.argv[2:])):
            print(line)
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "digest":
        data = collect()
        for name in data["failed"]:
            print(f"warning: {name} failed, skipped", file=sys.stderr)
        path = write_digest(data)
        print(f"wrote {path}")
        return 0

    today = date.today().isoformat()
    print(f"# News digest — {today}")
    print()

    data = collect()
    for name in ("Hacker News (front page)", "Lobsters", "Anthropic (anthropic.com/news)"):
        print(f"## {name}")
        if name in data["failed"]:
            print("- fetch failed (network / bot protection) — check manually")
        else:
            for title, _, score in data[name]:
                print(f"- {title} ({score} pts)" if score else f"- {title}")
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
