# Repo hosting services (GitHub, GitLab)
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: roadmap.sh, GitHub Docs, GitLab Docs

## What it is

The roadmap's fourth step: the remote home for your git repositories. Git
gives you version control locally; hosting gives you a shared origin,
pull requests/code review, issue tracking, and CI/CD hooks. GitHub and
GitLab are the two the roadmap names.

## The concepts

- **GitHub** — the largest community, default home of open source; PR review
  workflow, Actions for CI, Pages for hosting. Personal recommendation.
- **GitLab** — self-hostable alternative, all-in-one DevOps (repo + CI +
  registry) in one product.

## How it works

The hosted repo is a `remote` your local git pushes to / pulls from. The
collaboration loop: fork or branch → commit → push → **pull request** →
review → merge → CI runs on the new code. Both platforms bolt on the same
git core; the differentiator is the workflow tooling around it.

## How it fails (review checklist)

- **Push before pull** — remote has commits you don't; `git pull --rebase`
  before `git push` (merge commits are fine, but rebase keeps history
  readable).
- **Force-pushing to shared branches** — rewrites other people's history;
  `push --force-with-lease` at most, on your own branch only.
- **Treating PR review as optional** — the review IS the value; the merge is
  an afterthought.
- **Permissions drift** — giving write access to a whole team invites
  accidents; least privilege.

## Build that proves it

Create a repo, add a collaborator, and take one PR through review to merge
with a working CI check. That's the whole drill.

## Drill

Goal: reproduce the "push before pull" rejection and the linear-rebase fix
with two local clones sharing one bare remote.

Steps:
1. Dependency: git. In a scratch dir: `git init --bare remote.git`, then
   `git clone remote.git alice` and `git clone remote.git bob`.
2. In `alice`: create `a.txt`, `git add .`, `git commit -m a`, `git push`.
3. In `bob`: create `b.txt`, commit, and try `git push` — it is rejected
   (`! [rejected] ... non-fast-forward`, "fetch first") because alice pushed a
   commit bob doesn't have.
4. In `bob`: `git pull --rebase`, then `git push`. Run `git log --oneline` —
   alice's commit is there and the history is one linear line (rebase, not a
   merge commit).

Self-check (pass/fail):
- Step 3 prints the `[rejected]`/`fetch first` message — you reproduced the
  failure the note warns about.
- After step 4, `git log --oneline` in `bob` contains alice's commit and
  `git push` succeeds.
- You can explain why `git push --force` on a shared branch is the danger the
  note calls out: it would discard alice's commit instead of rebasing onto it.

Why this matters: PR/review workflows live on a shared remote; push-before-pull
and force-push are the failures that waste a review cycle.

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Repo Hosting Services" step
  (fetched Aug 3 2026)
- GitHub Docs, https://docs.github.com/en/get-started (fetched Aug 3 2026)
- GitLab Docs, https://docs.gitlab.com/ (fetched Aug 3 2026)
