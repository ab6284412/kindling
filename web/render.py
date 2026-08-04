"""Markdown rendering, content-path safety, and structure parsing."""
from __future__ import annotations

import os
import re

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories whose .md files are browseable through /content/<path>.
BROWSE_DIRS = ("concepts", "knowledge", "notes", "builds", "dsa", "soft-skills")
ROOT_FILES = ("learning.md", "news-ledger.md", "followups.md")

_md = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists"])

# Bare URLs -> links (the autolink extension isn't bundled with this Markdown build).
_URL = re.compile(r"https?://[^\s<)]+")
_SKIP_TAGS = re.compile(r"<(?:a|pre|code|script|style)\b[^>]*>.*?</(?:a|pre|code|script|style)>", re.S)


def _linkify(html: str) -> str:
    def repl(m: re.Match) -> str:
        url = m.group(0).rstrip(".,;:!?")
        return f'<a href="{url}">{url}</a>'

    out: list[str] = []
    pos = 0
    for keep in _SKIP_TAGS.finditer(html):
        out.append(_URL.sub(repl, html[pos : keep.start()]))
        out.append(keep.group(0))
        pos = keep.end()
    out.append(_URL.sub(repl, html[pos:]))
    return "".join(out)


# An <a href="..."> whose target is a relative .md/.html path.
_A_HREF = re.compile(r'<a\b([^>]*?)\bhref="([^"]+)"([^>]*)>')


def _rewrite_links(html: str, base_dir: str) -> str:
    """Rewrite relative .md links to /content/<path>, resolved against base_dir.

    base_dir is the repo-relative directory of the source file ('' for root
    files like learning.md). Absolute/URL/anchor/mailto targets are left alone.
    """

    def rew(m: re.Match) -> str:
        href = m.group(2)
        if href.startswith(("http://", "https://", "/", "#", "mailto:")):
            return m.group(0)
        rel = href.split("#", 1)[0]
        frag = f"#{href.split('#', 1)[1]}" if "#" in href else ""
        if not rel.endswith(".md"):
            return m.group(0)
        joined = os.path.normpath(os.path.join(base_dir, rel))
        # Must stay inside the repo and point at a real browseable file.
        if joined.startswith("..") or resolve_content_path(joined) is None:
            return m.group(0)
        return f'<a{m.group(1)}href="/content/{joined}{frag}"{m.group(3)}>'

    return _A_HREF.sub(rew, html)


def render_markdown(text: str, base_dir: str = "") -> str:
    return _rewrite_links(_linkify(_md.reset().convert(text)), base_dir)


def resolve_content_path(rel: str) -> str | None:
    """Map a URL path like 'concepts/http.md' to an absolute file path, or None.

    Only files inside BROWSE_DIRS (and ROOT_FILES) are reachable; any '..' or
    absolute segment is rejected outright.
    """
    rel = rel.strip().strip("/")
    if not rel:
        return None
    parts = rel.split("/")
    if any(p in ("", ".", "..") or "\\" in p for p in parts):
        return None
    if len(parts) == 1:
        if rel not in ROOT_FILES:
            return None
    elif parts[0] not in BROWSE_DIRS:
        return None
    if not rel.endswith(".md"):
        return None
    path = os.path.join(ROOT, *parts)
    if not os.path.isfile(path):
        return None
    return path


def list_content(dirname: str) -> list[str]:
    """Markdown files in a content dir, sorted, excluding its README.

    Concepts and DSA follow roadmap order (position in the dir's README
    catalogue); anything not catalogued sorts to the end, alphabetically.
    """
    base = os.path.join(ROOT, dirname)
    if not os.path.isdir(base):
        return []
    names = sorted(
        n
        for n in os.listdir(base)
        if n.endswith(".md") and n.lower() != "readme.md"
    )
    if dirname in ("concepts", "dsa"):
        names = _roadmap_order(names, dirname)
    return [f"{dirname}/{n}" for n in names]


def _roadmap_order(names: list[str], dirname: str) -> list[str]:
    index = []
    try:
        with open(os.path.join(ROOT, dirname, "README.md"), encoding="utf-8") as f:
            for m in re.finditer(r"\(([a-z0-9-]+\.md)\)", f.read()):
                name = m.group(1)
                if name not in index:
                    index.append(name)
    except OSError:
        return names
    by_pos = {name: i for i, name in enumerate(index)}
    return sorted(names, key=lambda n: by_pos.get(n, len(index)))


def parse_stages(text: str) -> list[str]:
    """Stage names from learning.md's `### N. <Title> [ ]` headings."""
    stages = []
    for m in re.finditer(
        r"(?m)^\s*###\s+\d+\.\s+(.+?)\s*`?\[[ xX]\]`?\s*$", text
    ):
        stages.append(m.group(1).strip())
    return stages


def _section(text: str, start: str, end: str) -> str | None:
    """Raw text of a section between heading lines. start/end are regexes."""
    m = re.search(start, text, flags=re.MULTILINE)
    if not m:
        return None
    rest = text[m.end():]
    if end:
        cut = re.search(end, rest, flags=re.MULTILINE)
        if cut:
            rest = rest[:cut.start()]
    return rest.strip()


# Matches "Self-check:" or "Self-check (pass/fail):" at line start.
_SELF_CHECK = r"^\s*Self-check.*?:"


def parse_drill(text: str) -> dict:
    """Extract title, goal, steps, self_check from a drill's existing markdown."""
    title = "Drill"
    tm = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if tm:
        title = tm.group(1).strip().replace("Drill:", "Drill:").strip()
    return {
        "title": title,
        "goal": _section(text, r"^Goal:\s*", r"^\s*Steps:"),
        "steps": _section(text, r"^\s*Steps:\s*", _SELF_CHECK),
        "self_check": _section(text, _SELF_CHECK, r"^\s*Why this matters:"),
    }
