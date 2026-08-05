"""Reference solution for builds/fastapi-crud.md — FastAPI + stdlib sqlite3, no ORM.

Run: uvicorn app:app  (or python3 -m uvicorn app:app)
"""
import sqlite3

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

app = FastAPI()
DB = "todo.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@app.on_event("startup")
def init_db() -> None:
    conn = sqlite3.connect(DB)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS todos ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " title TEXT NOT NULL,"
        " done INTEGER NOT NULL DEFAULT 0)"
    )
    conn.commit()
    conn.close()


class TodoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    done: bool = False


class TodoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = None
    done: bool | None = None


def _row(db, tid: int) -> dict | None:
    row = db.execute("SELECT id, title, done FROM todos WHERE id = ?", (tid,)).fetchone()
    return dict(row) if row else None


@app.get("/todos", response_model=list[dict])
def list_todos(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("SELECT id, title, done FROM todos ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@app.post("/todos", status_code=201)
def create_todo(body: TodoCreate, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        "INSERT INTO todos (title, done) VALUES (?, ?)", (body.title, int(body.done))
    )
    db.commit()
    return _row(db, cur.lastrowid)


@app.get("/todos/{tid}", response_model=dict)
def get_todo(tid: int, db: sqlite3.Connection = Depends(get_db)):
    row = _row(db, tid)
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    return row


@app.patch("/todos/{tid}", response_model=dict)
def update_todo(tid: int, body: TodoUpdate, db: sqlite3.Connection = Depends(get_db)):
    row = _row(db, tid)
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    fields, params = [], []
    if body.title is not None:
        fields.append("title = ?")
        params.append(body.title)
    if body.done is not None:
        fields.append("done = ?")
        params.append(int(body.done))
    if fields:
        db.execute(
            f"UPDATE todos SET {', '.join(fields)} WHERE id = ?", (*params, tid)
        )
        db.commit()
    return _row(db, tid)


@app.delete("/todos/{tid}", status_code=204)
def delete_todo(tid: int, db: sqlite3.Connection = Depends(get_db)):
    row = _row(db, tid)
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    db.execute("DELETE FROM todos WHERE id = ?", (tid,))
    db.commit()
    return None
