# SQL transactions and ACID
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: The PostgreSQL Global Development Group

## What it is

A transaction bundles multiple SQL statements into a single **all-or-nothing**
operation: either every statement takes effect, or none does. Its
intermediate states are invisible to other concurrent transactions, and
nothing is acknowledged as durable until it is on disk. "ACID" is the
acronym for these guarantees: **Atomicity, Consistency, Isolation, Durability**
(PostgreSQL's docs spell out the first, third, and fourth directly).

## How it works

- **Atomicity:** a group of updates is atomic — from the point of view of
  other transactions it happens completely or not at all. PostgreSQL's docs
  use the bank transfer: debit Alice, credit Bob, update branch totals. If
  anything fails partway, none of the steps take effect.
- **Isolation:** an open transaction's changes are invisible to others until
  `COMMIT`, at which point they all appear simultaneously. A concurrent
  "total branch balances" query never sees the debit without the credit.
- **Durability:** the database logs all updates to permanent storage *before*
  reporting the transaction complete — a crash right after "success" cannot
  lose the write.
- **The mechanics:** wrap statements in `BEGIN;` … `COMMIT;`, or abort with
  `ROLLBACK;`. PostgreSQL wraps *every* single statement in an implicit
  `BEGIN`/`COMMIT`, so each statement is itself a transaction unless you group
  them explicitly.
- **Savepoints** (`SAVEPOINT x` / `ROLLBACK TO x`) let you discard *part* of a
  transaction and keep the rest — and `ROLLBACK TO` is the only way to regain
  control of a transaction block that an error put into the aborted state.

## How it fails (review checklist)

- **Forgotten `COMMIT`** (or autocommit off in a driver): a long-open
  transaction holds locks and blocks others, and may never become visible.
- **Split-brain updates:** read-check-write patterns (e.g. "check balance,
  then debit") outside one transaction race with each other — classic lost
  update. The check and the write belong in the same `BEGIN`…`COMMIT`, or the
  DB needs row locks / `SELECT ... FOR UPDATE`.
- **Assuming every statement autocommits** when a driver or ORM (SQLAlchemy
  session) silently wraps work in a transaction you never committed — data
  "disappears" on disconnect.
- **Reporting success before durability:** without a real `COMMIT`/connection
  teardown, a client may be told it worked when the transaction never landed.
- **Long transactions cause bloat and contention** on busy tables — commit
  early, keep transactions short.

## Build that proves it

No build yet (this pass is concepts + drills). Short rep: the `## Drill`
below.

## Drill

Goal: see atomicity and isolation with your own eyes using stdlib SQLite.

Steps:
1. From a scratch dir, run `python3` (stdlib `sqlite3` — no installs):
   ```python
   import sqlite3
   c = sqlite3.connect("tx.db")
   c.execute("CREATE TABLE acct(name TEXT PRIMARY KEY, bal INTEGER)")
   c.execute("INSERT INTO acct VALUES ('alice', 100), ('bob', 100)")
   c.commit()
   ```
2. Open a second connection `d = sqlite3.connect("tx.db")` (a *separate*
   session). Query `SELECT * FROM acct` on `d` and on `c` — both see 200/2.
3. On `c`, start a transaction manually, debit Alice, credit Bob — then abort
   *before* committing:
   ```python
   c.execute("BEGIN")
   c.execute("UPDATE acct SET bal = bal - 10 WHERE name='alice'")
   c.execute("UPDATE acct SET bal = bal + 10 WHERE name='bob'")
   c.rollback()
   ```
4. Now read again from `c` and from `d`. Both must still show `alice=100`,
   `bob=100`. This proves the partial state was atomic (rolled back) and that
   the intermediate state was invisible to the other session.
5. Repeat step 3 but end with `c.commit()` and confirm the balances are now
   `90`/`110` and *visible from `d`* — the change appears to other sessions
   only as one unit, at commit.

Self-check (pass/fail — run it alone):
- After the `rollback()` run, both connections report `alice=100, bob=100`
  (no half-applied transfer).
- You can explain why `d` could never see `alice=90, bob=100` (invisible
  intermediate state) and why the committed run is visible from `d` only
  after commit (isolation + atomic visibility).
- Swap the order — write one UPDATE without `BEGIN` and confirm it *does*
  persist (implicit per-statement transaction).

Why this matters: money/balance logic is the canonical case; "transfer half
applied" and "check-then-write races" are the exact bugs transactions exist to
prevent — and the same rules hold in Postgres and in your ORM.

## Further reading
- The PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/tutorial-transactions.html —
  "3.4. Transactions", PostgreSQL 18 docs (fetched Aug 3 2026)
- The PostgreSQL Global Development Group,
  https://www.postgresql.org/docs/current/mvcc.html — "Concurrency Control"
  (isolation of concurrent transactions, fetched Aug 3 2026)
