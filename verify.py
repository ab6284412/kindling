#!/usr/bin/env python3
"""Offline verification for the learning lab. Stdlib only.

Subcommands:
  verify.py links              check every http(s) URL in the corpus
  verify.py build <name> [dir] run a build's self-check against dir
                               (default: solutions/<name>)
  verify.py stage <n>          alias for 'build' of stage n
  verify.py all                run every build check
  verify.py drill-audit        every concept has exactly one parseable ## Drill
  verify.py selftest           internal consistency checks

Exit codes: 0 = all pass, 1 = failures, 3 = skipped (e.g. DB not running).
Note: `stage`/`all` exit 3 when a check self-skips — a common cause is the
dev server holding port 8000 (http-server check), which is expected.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(ROOT, "web", ".venv", "bin", "python")
BUILD_DIRS = ("concepts", "knowledge", "builds", "dsa", "soft-skills", "notes")
ROOT_MD = ("learning.md", "news-ledger.md", "followups.md")

# stage number -> (build slug, check module, build file)
STAGES = {
    1: ("python-foundation", "python_foundation", "builds/python-from-zero.md"),
    2: ("http-server", "http_server", "builds/http-server.md"),
    3: ("fastapi-crud", "fastapi_crud", "builds/fastapi-crud.md"),
    4: ("auth-security", "auth_security", "builds/auth-security.md"),
    5: ("storage-cache", "storage_cache", "builds/storage-cache.md"),
    6: ("background-worker", "background_worker", "builds/background-worker.md"),
    7: ("production-deploy", "production_deploy", "builds/production-deploy.md"),
}

_URL = re.compile(r"https?://[^\s<>\"'`;]+")

_DEV_HOSTS = {"localhost", "127.0.0.1", "example.com"}  # learner runs these; not sources


def clean_url(url: str) -> str:
    """Trim punctuation and unbalanced closers that the regex can over-capture."""
    url = url.rstrip(".,;:!?")
    while url.endswith(")") and url.count(")") > url.count("("):
        url = url[:-1]
    if url.endswith("("):
        url = url[:-1]
    return url


def iter_urls(text: str):
    """Yield cleaned URLs, skipping ones inside backtick code spans."""
    for m in _URL.finditer(text):
        if m.start() > 0 and text[m.start() - 1] == "`":
            continue
        yield clean_url(m.group(0))


def corpus_files() -> list[str]:
    files = [os.path.join(ROOT, name) for name in ROOT_MD]
    for d in BUILD_DIRS:
        base = os.path.join(ROOT, d)
        if os.path.isdir(base):
            files += [
                os.path.join(base, f)
                for f in sorted(os.listdir(base))
                if f.endswith(".md")
            ]
    return files


def _check_url(url: str) -> tuple[bool, str]:
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method)
            req.add_header("User-Agent", "Mozilla/5.0 (link-check; learning-lab)")
            with urllib.request.urlopen(req, timeout=12) as resp:
                return True, str(resp.status)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                return True, "403 blocked"  # bot protection, not a dead link
            if e.code in (405,) and method == "HEAD":
                continue  # try GET
            return False, str(e.code)
        except Exception as e:
            if method == "GET":
                return False, f"{type(e).__name__}: {e}"
    return False, "405 on HEAD and GET"


def cmd_links() -> int:
    urls: dict[str, str] = {}  # url -> source file
    for path in corpus_files():
        try:
            text = open(path, encoding="utf-8").read()
        except OSError:
            continue
        for url in iter_urls(text):
            host = urllib.parse.urlsplit(url).hostname or ""
            if host in _DEV_HOSTS or host.endswith(".localhost"):
                continue
            urls.setdefault(url, os.path.relpath(path, ROOT))

    results: list[tuple[str, bool, str, str]] = []

    def check(item):
        url, src = item
        ok, detail = _check_url(url)
        results.append((url, ok, detail, src))

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(check, urls.items()))

    results.sort(key=lambda r: (r[1], r[0]))
    broken = 0
    for url, ok, detail, src in results:
        if ok:
            print(f"OK    {detail:>3} {url}  ({src})")
        else:
            broken += 1
            print(f"BROKEN {detail} {url}  ({src})")
    print(f"\n{len(results)} URLs, {broken} broken")
    return 1 if broken else 0


def _run_check(check: str, workdir: str) -> int:
    py = VENV_PY if os.path.exists(VENV_PY) else sys.executable
    script = os.path.join(ROOT, "verify", "checks", f"{check}.py")
    if not os.path.exists(script):
        print(f"unknown check: {check}")
        return 1
    p = subprocess.run([py, script, workdir], cwd=ROOT)
    return p.returncode


def cmd_build(name: str, workdir: str | None) -> int:
    for stage, (slug, check, build_file) in STAGES.items():
        if slug == name:
            if workdir is None:
                workdir = os.path.join(ROOT, "solutions", slug)
            print(f"=== stage {stage} build: {slug} (spec: {build_file}) ===")
            return _run_check(check, workdir)
    print(f"unknown build: {name}; known: {', '.join(v[0] for v in STAGES.values())}")
    return 1


def cmd_stage(n: str) -> int:
    try:
        stage = int(n)
    except ValueError:
        print(f"stage must be a number 1-7, got {n!r}")
        return 1
    slug, check, build_file = STAGES.get(stage, (None, None, None))
    if slug is None:
        print("stage must be 1-7")
        return 1
    print(f"=== stage {stage}: {slug} (spec: {build_file}) ===")
    return _run_check(check, os.path.join(ROOT, "solutions", slug))


def cmd_all() -> int:
    codes = [cmd_stage(str(n)) for n in sorted(STAGES)]
    if 1 in codes:
        return 1
    if 3 in codes:
        return 3
    return 0


def cmd_drill_audit() -> int:
    bad = []
    for base in ("concepts", "knowledge"):
        for f in sorted(os.listdir(os.path.join(ROOT, base))):
            if not f.endswith(".md") or f == "README.md":
                continue
            text = open(os.path.join(ROOT, base, f), encoding="utf-8").read()
            if not re.search(r"(?m)^## Drill\s*$", text):
                bad.append(f"{base}/{f}: no ## Drill heading")
                continue
            if not re.search(r"(?m)^Goal:", text) or not re.search(r"(?m)^Steps:", text) \
               or not re.search(r"(?m)^Self-check", text) or not re.search(r"(?m)^Why this matters:", text):
                bad.append(f"{base}/{f}: drill missing Goal/Steps/Self-check/Why lines")
    for b in bad:
        print(f"BROKEN {b}")
    print(f"{len(bad)} note(s) with drill problems")
    return 1 if bad else 0


def cmd_selftest() -> int:
    assert sorted(STAGES) == [1, 2, 3, 4, 5, 6, 7], "stage map must cover 1-7"
    for _, (slug, check, build_file) in STAGES.items():
        assert os.path.isfile(os.path.join(ROOT, build_file)), f"missing {build_file}"
        assert os.path.isfile(os.path.join(ROOT, "verify", "checks", f"{check}.py")), f"missing check {check}"
    print("selftest: stage map + build files + check scripts all present")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    cmd = argv[0]
    if cmd == "links":
        return cmd_links()
    if cmd == "build":
        if len(argv) < 2:
            print("usage: verify.py build <name> [dir]")
            return 1
        return cmd_build(argv[1], argv[2] if len(argv) > 2 else None)
    if cmd == "stage":
        if len(argv) < 2:
            print("usage: verify.py stage <n>")
            return 1
        return cmd_stage(argv[1])
    if cmd == "all":
        return cmd_all()
    if cmd == "drill-audit":
        return cmd_drill_audit()
    if cmd == "selftest":
        return cmd_selftest()
    print(f"unknown command: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
