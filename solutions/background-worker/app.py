"""Reference solution for builds/background-worker.md.

FastAPI + stdlib queue/threads: POST /todos enqueues a slow job and returns 202;
a worker thread runs it and POSTs a completion webhook back to the API's own
/webhooks/local endpoint over real HTTP (urllib, stdlib).

Queued jobs are lost on restart — that's the build's stated v1 trade-off
(durable broker is the extension).
"""
import json
import os
import queue
import threading
import time
import urllib.request

import psycopg
from fastapi import Depends, FastAPI, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel, ConfigDict

app = FastAPI()
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:p@localhost:5432/postgres"
)
WEBHOOK_URL = os.environ.get(
    "WEBHOOK_URL", "http://127.0.0.1:8000/webhooks/local"
)
_jobs: queue.Queue = queue.Queue()


def get_db():
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        yield conn


def _conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@app.on_event("startup")
def init_db() -> None:
    with _conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS todos ("
            " id SERIAL PRIMARY KEY,"
            " title TEXT NOT NULL,"
            " done BOOLEAN NOT NULL DEFAULT FALSE)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS jobs ("
            " id SERIAL PRIMARY KEY,"
            " todo_id INTEGER NOT NULL,"
            " status TEXT NOT NULL,"
            " created_at TIMESTAMPTZ NOT NULL DEFAULT now(),"
            " finished_at TIMESTAMPTZ)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS webhooks ("
            " id SERIAL PRIMARY KEY,"
            " todo_id INTEGER NOT NULL,"
            " payload TEXT NOT NULL,"
            " received_at TIMESTAMPTZ NOT NULL DEFAULT now())"
        )
        conn.commit()
    threading.Thread(target=worker, daemon=True).start()


def deliver_webhook(todo_id: int, payload: dict) -> None:
    """Real HTTP POST to the API's own receiver — the actual worker behavior."""
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req, timeout=5).read()  # non-2xx raises here


def worker() -> None:
    while True:
        job_id = _jobs.get()
        try:
            with _conn() as conn:
                conn.execute("UPDATE jobs SET status = 'running' WHERE id = %s", (job_id,))
                conn.commit()
                todo_id = conn.execute(
                    "SELECT todo_id FROM jobs WHERE id = %s", (job_id,)
                ).fetchone()["todo_id"]
            time.sleep(3)  # simulated slow side effect (send email / generate PDF)
            with _conn() as conn:
                conn.execute(
                    "UPDATE jobs SET status = 'done', finished_at = now()"
                    " WHERE id = %s",
                    (job_id,),
                )
                conn.commit()
            deliver_webhook(todo_id, {"job_id": job_id, "todo_id": todo_id, "status": "done"})
        except Exception:
            with _conn() as conn:
                conn.execute(
                    "UPDATE jobs SET status = 'failed', finished_at = now()"
                    " WHERE id = %s",
                    (job_id,),
                )
                conn.commit()
        finally:
            _jobs.task_done()


class TodoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    done: bool = False


@app.get("/todos", response_model=list[dict])
def list_todos(db: psycopg.Connection = Depends(get_db)):
    return db.execute("SELECT id, title, done FROM todos ORDER BY id").fetchall()


@app.post("/todos", status_code=202)
def create_todo(body: TodoCreate, db: psycopg.Connection = Depends(get_db)):
    cur = db.execute(
        "INSERT INTO todos (title, done) VALUES (%s, %s) RETURNING id",
        (body.title, body.done),
    )
    tid = cur.fetchone()["id"]
    job = db.execute(
        "INSERT INTO jobs (todo_id, status) VALUES (%s, 'queued') RETURNING id",
        (tid,),
    )
    db.commit()
    job_id = job.fetchone()["id"]
    _jobs.put(job_id)  # off the request path — return before the work runs
    return {"job_id": job_id}


@app.get("/jobs/{job_id}", response_model=dict)
def get_job(job_id: int, db: psycopg.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM jobs WHERE id = %s", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    return row


@app.get("/webhooks", response_model=list[dict])
def list_webhooks(db: psycopg.Connection = Depends(get_db)):
    return db.execute("SELECT * FROM webhooks ORDER BY id").fetchall()


@app.post("/webhooks/local", status_code=201)
def webhook_receiver(body: dict, db: psycopg.Connection = Depends(get_db)):
    """Receives the worker's completion POST and records the delivery."""
    todo_id = int(body.get("todo_id", 0))
    db.execute(
        "INSERT INTO webhooks (todo_id, payload) VALUES (%s, %s)",
        (todo_id, json.dumps(body)),
    )
    db.commit()
    return {"ok": True}
