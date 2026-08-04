# Rubber duck debugging

Created 2026-08-03 · Provenance: AI-drafted · Credits: The Pragmatic Programmer

## Summary

Explain your problem out loud, step by step, to an inanimate object (a duck,
a coworker's chair, your terminal window). The act of narrating forces your
brain to linearize the assumption soup — the bug usually reveals itself mid-
sentence, before the duck "answers".

## Lesson

1. Your internal monologue skips the step you got wrong. Speaking forces it
   back into the chain.
2. Protocol: state the *expected* behavior, the *actual* behavior, and the
   steps between — at the first gap you feel uneasy, that's the bug.
3. Write the narration into a chat/note first. If the explanation is harder
   to write than it should be, the model of the bug is wrong.

## Drill

Self-check: next bug you debug for >10 minutes, write one paragraph: "I expect
X, I get Y, between them my program does Z." If the paragraph has a gap you
can't fill, find it — that gap is the bug.

## Further reading

- https://en.wikipedia.org/wiki/Rubber_duck_debugging
