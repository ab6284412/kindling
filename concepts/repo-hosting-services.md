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

## Further reading
- roadmap.sh, https://roadmap.sh/backend — "Repo Hosting Services" step
  (fetched Aug 3 2026)
- GitHub Docs, https://docs.github.com/en/get-started (fetched Aug 3 2026)
- GitLab Docs, https://docs.gitlab.com/ (fetched Aug 3 2026)
