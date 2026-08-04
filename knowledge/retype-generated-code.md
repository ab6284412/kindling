# Retype generated code by hand
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: Ankur Sethi

## Summary
HN discussion (93 pts): "Prevent cognitive debt by manually retyping
LLM-generated code." Same argument as retyping library examples — typing forces
you to actually read each token; pasting lets you skip comprehension.

## Lesson
For every block of generated code you keep: retype it, comment each line, then
delete your typing and paste only once you can explain it. The lines you retype
wrong are exactly the lines you don't understand. Cheapest comprehension check
that exists.

## Drill

Goal: prove you understand generated code before you keep it.

Steps:
1. Generate a 15–30 line function (any tool) that you actually plan to keep.
2. Cover it. Retype it from memory, no peeking.
3. Uncover, diff your version against the original.
4. Every line you got wrong is a line you didn't understand. Comment those
   lines: what were they doing and why are they there?
5. Delete your retyped version; paste the original only after you can explain it.

Self-check: cover a random line and say what breaks without the model open.

Why this matters: pasting without reading is how cognitive debt builds — code
you keep but can't explain is code you'll debug at 3am.

## Further reading
- Ankur Sethi, https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/ — "Prevent cognitive debt by manually retyping LLM-generated code" (Aug 2 2026; ~100 pts on HN Aug 3)
