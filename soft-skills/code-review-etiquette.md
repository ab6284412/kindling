# Code review etiquette

Created 2026-08-03 · Provenance: AI-drafted · Credits: Google eng-practices

## Summary

Reviews are conversations about the code, not verdicts on the author. The
Google eng-practices playbook: comments should be *necessary*, kind, and
specific; prefer asking questions ("is this the right trade?" ) over orders
("change this"). The author replies to every comment; the reviewer approves
when the main points are resolved.

## Lesson

1. Reviewer: name the *behavior* problem ("this mutates shared state") and
   propose a direction — not just "this is wrong."
2. Author: treat comments as data. Push back with reasons, not ego; default to
   "that's a fair point" when the reviewer is right.
3. Small PRs get better reviews. A 400-line diff is a review-behavior change;
   split work instead.

## Drill

Self-check: find a PR you wrote (or a hypothetical one) and write two review
comments about it: one question-form, one that names a specific behavior.
Neither may contain "you".

## Further reading

- https://google.github.io/eng-practices/review/ (Google code review guidance)
