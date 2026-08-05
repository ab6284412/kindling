"""Reference solution for builds/storage-cache.md — Postgres + coherent dict cache.

Requires Postgres (docker run --rm -e POSTGRES_PASSWORD=p -p 5432:5432 postgres:16)
and psycopg. Point DATABASE_URL at it, then: uvicorn app:app
"""
import os

import psycopg
from fastapi import Depends, FastAPI, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel, ConfigDict

app = FastAPI()
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:p@localhost:5432/postgres"
)
DB_ONLY = os.environ.get("DB_ONLY") == "1"  # spec's db-only turn: disable the cache
_cache: dict[int, dict] = {}  # todo_id -> row; in-process cache-aside


def get_db():
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        yield conn


@app.on_event("startup")
def init_db() -> None:
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS todos ("
            " id SERIAL PRIMARY KEY,"
            " title TEXT NOT NULL UNIQUE,"
            " done BOOLEAN NOT NULL DEFAULT FALSE)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS audit_log ("
            " id SERIAL PRIMARY KEY,"
            " todo_id INTEGER NOT NULL REFERENCES todos(id) ON DELETE CASCADE,"
            " action TEXT NOT NULL)"
        )
        conn.commit()


class TodoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    done: bool = False


class TodoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = None
    done: bool | None = None


def _load(db, tid: int) -> dict | None:
    row = db.execute("SELECT id, title, done FROM todos WHERE id = %s", (tid,)).fetchone()
    return row if row else None


@app.get("/todos", response_model=list[dict])
def list_todos(db: psycopg.Connection = Depends(get_db)):
    return db.execute("SELECT id, title, done FROM todos ORDER BY id").fetchall()


@app.post("/todos", status_code=201)
def create_todo(body: TodoCreate, db: psycopg.Connection = Depends(get_db)):
    try:
        # One transaction: the row AND its audit line land together or not at all.
        cur = db.execute(
            "INSERT INTO todos (title, done) VALUES (%s, %s) RETURNING id",
            (body.title, body.done),
        )
        tid = cur.fetchone()["id"]
        db.execute(
            "INSERT INTO audit_log (todo_id, action) VALUES (%s, %s)",
            (tid, "created"),
        )
        db.commit()
    except psycopg.errors.UniqueViolation:
        db.rollback()
        raise HTTPException(status_code=409, detail="title taken") from None
    return _load(db, tid)


@app.get("/todos/{tid}", response_model=dict)
def get_todo(tid: int, db: psycopg.Connection = Depends(get_db)):
    if not DB_ONLY:
        hit = _cache.get(tid)
        if hit is not None:
            return hit  # cache hit — no DB round trip
    row = _load(db, tid)
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    if not DB_ONLY:
        _cache[tid] = row  # cache-aside: populate on miss
    return row


@app.patch("/todos/{tid}", response_model=dict)
def update_todo(tid: int, body: TodoUpdate, db: psycopg.Connection = Depends(get_db)):
    row = _load(db, tid)
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    fields, params = [], []
    if body.title is not None:
        fields.append("title = %s")
        params.append(body.title)
    if body.done is not None:
        fields.append("done = %s")
        params.append(body.done)
    if fields:
        db.execute(
            f"UPDATE todos SET {', '.join(fields)} WHERE id = %s", (*params, tid)
        )
        db.commit()
    row = _load(db, tid)
    if not DB_ONLY:
        _cache.pop(tid, None)  # evict AFTER commit — a rolled-back write stays stale-safe
    return row


@app.delete("/todos/{tid}", status_code=204)
def delete_todo(tid: int, db: psycopg.Connection = Depends(get_db)):
    row = _load(db, tid)
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    db.execute("DELETE FROM todos WHERE id = %s", (tid,))
    db.commit()
    _cache.pop(tid, None)
    return None
