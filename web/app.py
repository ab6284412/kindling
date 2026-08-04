"""Local study portal. Run: uvicorn web.app:app --reload"""
from __future__ import annotations

import os
import re
import threading

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from . import render, state

app = FastAPI(title="Tech Research & Learning Lab")
app.mount("/static", StaticFiles(directory=os.path.join(render.ROOT, "web/static")), name="static")
templates = Jinja2Templates(directory=os.path.join(render.ROOT, "web/templates"))

_lock = threading.Lock()  # ponytail: global lock, fine for one local user


class ToggleBody(BaseModel):
    kind: str
    path: str


class NoteBody(BaseModel):
    path: str
    text: str


def _read(name: str) -> str:
    with open(os.path.join(render.ROOT, name), encoding="utf-8") as f:
        return f.read()


def _stages() -> list[str]:
    return render.parse_stages(_read("learning.md"))


def _valid_stage(name: str) -> bool:
    return name in _stages()


def _valid_content(rel: str) -> bool:
    return render.resolve_content_path(rel) is not None


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    s = state.load()
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "stages": _stages(),
            "state": s,
            "stages_done": sum(1 for v in s["stages"].values() if v),
            "drills_done": sum(1 for v in s["drills"].values() if v),
            "reads_done": sum(1 for v in s["reads"].values() if v),
            "pillars": _pillar_counts(),
            "news_count": _news_count(),
        },
    )


def _pillar_counts() -> list[tuple[str, str, int]]:
    return [(slug, title, len(render.list_content(slug))) for slug, title in PILLARS]


def _news_count() -> int:
    text = _read("news-ledger.md")
    return len(re.findall(r"(?m)^\|\s+\d{4}-", text))


@app.get("/learning", response_class=HTMLResponse)
def learning(request: Request):
    return templates.TemplateResponse(
        request,
        "learning.html",
        {
            "stages": _stages(),
            "html": render.render_markdown(_read("learning.md")),
            "state": state.load(),
        },
    )


PILLARS = (
    ("concepts", "Concepts"),
    ("knowledge", "Knowledge"),
    ("notes", "Notes"),
    ("builds", "Builds"),
    ("dsa", "DSA interview prep"),
    ("soft-skills", "Soft skills"),
)

READABLE_PREFIXES = ("concepts/", "knowledge/", "dsa/", "soft-skills/")


@app.get("/concepts", response_class=HTMLResponse)
@app.get("/knowledge", response_class=HTMLResponse)
@app.get("/notes", response_class=HTMLResponse)
@app.get("/builds", response_class=HTMLResponse)
@app.get("/dsa", response_class=HTMLResponse)
@app.get("/soft-skills", response_class=HTMLResponse)
def pillar(request: Request, pillar: str = ""):
    if not pillar:
        pillar = request.url.path.strip("/")
    title = dict(PILLARS).get(pillar)
    if title is None:
        raise HTTPException(status_code=404, detail="Unknown pillar")
    return templates.TemplateResponse(
        request,
        "list.html",
        {
            "pillar": pillar,
            "title": title,
            "items": render.list_content(pillar),
            "state": state.load(),
        },
    )


@app.get("/news", response_class=HTMLResponse)
def news(request: Request):
    return templates.TemplateResponse(
        request,
        "content.html",
        {
            "path": "news-ledger.md",
            "title": "News ledger",
            "html": render.render_markdown(_read("news-ledger.md")),
            "is_drill": False,
            "is_readable": False,
            "state": state.load(),
        },
    )


def _title_of(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return m.group(1).strip() if m else ""


@app.get("/content/{path:path}", response_class=HTMLResponse)
def content(request: Request, path: str):
    abs_path = render.resolve_content_path(path)
    if abs_path is None:
        raise HTTPException(status_code=404, detail="Not found")
    text = _read_abs(abs_path)
    is_drill = bool(re.search(r"(?m)^## Drill\s*$", text))
    drill = None
    if is_drill:
        drill = {
            k: render.render_markdown(v) if v else None
            for k, v in render.parse_drill(text).items()
        }
    context = {
        "path": path,
        "title": _title_of(text),
        "html": render.render_markdown(text, base_dir=os.path.dirname(path)),
        "drill": drill,
        "is_drill": is_drill,
        "is_readable": path.startswith(READABLE_PREFIXES),
        "state": state.load(),
        "pillar_title": None,
        "prev_item": None,
        "next_item": None,
    }
    parts = path.split("/")
    if len(parts) == 2:
        pillar = parts[0]
        items = render.list_content(pillar)
        try:
            i = items.index(path)
        except ValueError:
            i = -1
        if i >= 0:
            context["pillar_title"] = dict(PILLARS).get(pillar, pillar.title())
            context["pillar_path"] = f"/{pillar}"
            context["prev_item"] = items[i - 1] if i > 0 else None
            context["next_item"] = items[i + 1] if i + 1 < len(items) else None
    return templates.TemplateResponse(request, "content.html", context)


@app.post("/api/toggle")
def api_toggle(body: ToggleBody) -> JSONResponse:
    if body.kind == "stage":
        if not _valid_stage(body.path):
            raise HTTPException(status_code=400, detail="Unknown stage")
    elif body.kind == "drill":
        if not _valid_content(body.path):
            raise HTTPException(status_code=400, detail="Unknown content")
    elif body.kind == "read":
        if not body.path.startswith(READABLE_PREFIXES) or not _valid_content(body.path):
            raise HTTPException(status_code=400, detail="Not readable content")
    else:
        raise HTTPException(status_code=400, detail="Unknown kind")
    with _lock:
        s = state.load()
        value = state.toggle(s, body.kind, body.path)
        state.save(s)
    return JSONResponse({"value": value})


@app.post("/api/note")
def api_note(body: NoteBody) -> JSONResponse:
    if not _valid_content(body.path):
        raise HTTPException(status_code=400, detail="Unknown content")
    with _lock:
        s = state.load()
        state.set_note(s, body.path, body.text)
        state.save(s)
    return JSONResponse({"ok": True})


def _read_abs(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()
