"""Reference solution for builds/auth-security.md.

Extends the stage-3 CRUD app (builds/fastapi-crud.md) with stdlib auth:
pbkdf2 password hashing, DB-backed session tokens, ownership checks.

Decision notes (why it does what the spec does):
- Sessions live in a `sessions` TABLE (not self-contained tokens), so auth is
  revocable and a restart wipes them — that's why /me 401s after restart. The
  spec asks for both "DB-backed" and "restart invalidates"; the startup handler
  recreating the sessions table satisfies both. A persistent session store is
  the extension.
- `extra="forbid"` on the auth Pydantic models is the "no mass assignment"
  OWASP check.
"""
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict

app = FastAPI()
DB = "todo.db"
PBKDF2_ITER = 210_000
SESSION_TTL = timedelta(days=7)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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
        "CREATE TABLE IF NOT EXISTS users ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " email TEXT UNIQUE NOT NULL,"
        " password_hash TEXT NOT NULL,"
        " salt TEXT NOT NULL,"
        " created_at TEXT NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS todos ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " title TEXT NOT NULL,"
        " done INTEGER NOT NULL DEFAULT 0,"
        " owner_id INTEGER NOT NULL REFERENCES users(id))"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS sessions ("
        " token TEXT PRIMARY KEY,"
        " user_id INTEGER NOT NULL REFERENCES users(id),"
        " expires_at TEXT NOT NULL)"
    )
    conn.execute("DELETE FROM sessions")  # fresh boot = no valid sessions
    conn.commit()
    conn.close()


class RegisterBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str
    password: str


class LoginBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str
    password: str


class TodoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    done: bool = False


class TodoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = None
    done: bool | None = None


def _public_user(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "email": row["email"], "created_at": row["created_at"]}


@app.post("/register", status_code=201)
def register(body: RegisterBody, db: sqlite3.Connection = Depends(get_db)):
    if not EMAIL_RE.match(body.email):
        raise HTTPException(status_code=422, detail="bad email")
    salt = os.urandom(16)
    pwhash = hashlib.pbkdf2_hmac("sha256", body.password.encode(), salt, PBKDF2_ITER)
    try:
        cur = db.execute(
            "INSERT INTO users (email, password_hash, salt, created_at)"
            " VALUES (?, ?, ?, ?)",
            (
                body.email,
                pwhash.hex(),
                salt.hex(),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="email taken") from None
    row = db.execute("SELECT id, email, created_at FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()
    return _public_user(row)


@app.post("/login")
def login(body: LoginBody, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute(
        "SELECT id, email, password_hash, salt FROM users WHERE email = ?",
        (body.email,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=401, detail="bad credentials")
    pwhash = hashlib.pbkdf2_hmac(
        "sha256", body.password.encode(), bytes.fromhex(row["salt"]), PBKDF2_ITER
    )
    if not hmac.compare_digest(pwhash.hex(), row["password_hash"]):
        raise HTTPException(status_code=401, detail="bad credentials")
    token = secrets.token_hex(32)
    expires = datetime.now(timezone.utc) + SESSION_TTL
    db.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
        (token, row["id"], expires.isoformat()),
    )
    db.commit()
    return {"token": token, "expires_at": expires.isoformat()}


def get_current_user(
    authorization: str | None = Header(default=None),
    db: sqlite3.Connection = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing token")
    token = authorization.split(" ", 1)[1]
    row = db.execute(
        "SELECT u.id, u.email, u.created_at, s.expires_at"
        " FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token = ?",
        (token,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=401, detail="invalid token")
    if datetime.fromisoformat(row["expires_at"]) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="expired token")
    return _public_user(row)


@app.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user


def _todo(db, tid: int) -> dict | None:
    row = db.execute(
        "SELECT id, title, done, owner_id FROM todos WHERE id = ?", (tid,)
    ).fetchone()
    return dict(row) if row else None


@app.get("/todos", response_model=list[dict])
def list_todos(db: sqlite3.Connection = Depends(get_db), user: dict = Depends(get_current_user)):
    rows = db.execute(
        "SELECT id, title, done, owner_id FROM todos ORDER BY id"
    ).fetchall()
    return [dict(r) for r in rows]


@app.post("/todos", status_code=201)
def create_todo(body: TodoCreate, db: sqlite3.Connection = Depends(get_db), user: dict = Depends(get_current_user)):
    cur = db.execute(
        "INSERT INTO todos (title, done, owner_id) VALUES (?, ?, ?)",
        (body.title, int(body.done), user["id"]),
    )
    db.commit()
    return _todo(db, cur.lastrowid)


@app.get("/todos/{tid}", response_model=dict)
def get_todo(tid: int, db: sqlite3.Connection = Depends(get_db), user: dict = Depends(get_current_user)):
    todo = _todo(db, tid)
    if todo is None:
        raise HTTPException(status_code=404, detail="not found")
    if todo["owner_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="forbidden")
    return todo


@app.patch("/todos/{tid}", response_model=dict)
def update_todo(tid: int, body: TodoUpdate, db: sqlite3.Connection = Depends(get_db), user: dict = Depends(get_current_user)):
    todo = _todo(db, tid)
    if todo is None:
        raise HTTPException(status_code=404, detail="not found")
    if todo["owner_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="forbidden")
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
    return _todo(db, tid)


@app.delete("/todos/{tid}", status_code=204)
def delete_todo(tid: int, db: sqlite3.Connection = Depends(get_db), user: dict = Depends(get_current_user)):
    todo = _todo(db, tid)
    if todo is None:
        raise HTTPException(status_code=404, detail="not found")
    if todo["owner_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="forbidden")
    db.execute("DELETE FROM todos WHERE id = ?", (tid,))
    db.commit()
    return None
