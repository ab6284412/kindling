# Version control systems (Git)
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, Scott Chacon & Ben Straub (Pro Git)

## What it is

The roadmap's third step: a version control system records every change to a
project so you can rewind, branch, and collaborate. Git is the tool; the
roadmap lists it as a personal recommendation and it is the de-facto standard.

## How it works

- A **commit** is a snapshot of the whole project, addressed by content hash
  (SHA-1). History is a graph of commits, so rewind is trivial.
- **Branches** are movable pointers to commits — cheap to create, which makes
  "branch per feature" the default workflow.
- A **working tree → index → commit** staging model: you choose which changes
  go into each commit.
- **Distributed:** every clone has the full history; no single point of
  failure (unlike SVN).
- The roadmap pairs it with **GitHub/GitLab** (see `repo-hosting-services.md`):
  git is the tool, hosting is the remote.

## How it fails (review checklist)

- **Committing secrets** — a `.env` in history stays in history even after
  you delete the file; scrub with `filter-repo`, then rotate the credential.
- **Huge binary/venv files in the repo** — every clone and fetch pays for
  them forever; use `.gitignore`.
- **Merge conflicts from parallel work** — unavoidable but shrinkable: small
  commits, rebase/merge early and often.
- **Not knowing staging vs. commit vs. push** — the classic junior failure is
  `git commit -m "x"` after `git add .` when only part was meant to go.

## Build that proves it

No git drill yet. The test: recreate a botched history —
commit a secret, remove it, and rewrite history to purge it from every
commit — and explain the hash chain while doing it.

## Drill

Goal: see the staging model, content-addressed storage, and a safe rewind with
your own git repo.

Steps:
1. In a scratch dir: `git init`, `printf 'v1\n' > a.txt`, `git add a.txt`,
   `git commit -m v1`.
2. Append a second line to `a.txt` and create `b.txt`. Stage only `a.txt`
   (`git add a.txt`) and run `git status --short` — you should see `M  a.txt`
   (staged) and `?? b.txt` (untracked). Commit, then `git log --oneline`
   shows two commits.
3. Undo the second commit safely: `git revert HEAD --no-edit`, then `cat a.txt`
   and `git log --oneline` — the file is back to one line but history gained a
   commit (nothing rewritten).
4. Content addressing: `printf 'hi\n' > c1.txt && printf 'hi\n' > c2.txt`,
   `git add .`, then `git ls-files -s` — c1.txt and c2.txt share the same blob
   hash, because identical content hashes to the same object.

Self-check (pass/fail):
- Step 2's `git status --short` shows exactly `M  a.txt` and `?? b.txt` — you
  can tell staged from untracked.
- After `git revert`, `a.txt` has one line, `git log --oneline` grew by one,
  and you can explain why this is safer than `git reset` on a shared branch.
- `git ls-files -s` lists c1.txt and c2.txt with the same hash.

Why this matters: "commit everything with `git add .`" and unsafe history
rewrites are the two classic junior failures this drill makes visible.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Version Control Systems" step
  (fetched Aug 3 2026)
- Scott Chacon and Ben Straub, https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control —
  "Getting Started — About Version Control", Pro Git (fetched Aug 3 2026)
