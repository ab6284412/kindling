# Big O notation

Created 2026-08-03 · Provenance: AI-drafted · Credits: Navdeep Singh (NeetCode), Yangshun Tay (Tech Interview Handbook)

## Summary

Big O classifies how an algorithm's work grows as input size `n` grows — it's a
*rate*, not a speedometer. Drop constants and lower-order terms: `3n + 40` is
`O(n)`. The common ladder (fastest → slowest):

- `O(1)` constant — hash lookup, array index
- `O(log n)` — halving at each step (binary search, balanced-tree lookup)
- `O(n)` — one pass over the input
- `O(n log n)` — the best general sort (merge/quick/heap sort)
- `O(n²)` — nested loops (naive bubble/selection sort)
- `O(2ⁿ)`, `O(n!)` — exponential/factorial; fine for tiny `n` only

## Lesson

1. Count the *dominant* operation — usually the loop depth times what happens
   inside.
2. A loop that shrinks by halves is `log n`; a loop over `n` that calls a
   `log n` helper is `n log n`.
3. Space complexity counts too — extra arrays/recursion depth.
4. Interview moves: state the complexity *before* the interviewer asks, then
   justify it in one sentence ("one pass over the array, so O(n) time,
   O(1) extra space").

## Drill

Self-check: for each of these, write the time and extra space, then expand:

- sum of a list of length `n`
- binary search in a sorted list
- checking for duplicates with a nested loop vs. a `set()`

Answers: O(n)/O(1), O(log n)/O(1), O(n²)/O(1) vs O(n)/O(n).

## Open questions

- When is an `O(n²)` solution actually the right one? (Small fixed `n`, or the
  constant factor of the "better" algorithm is huge.)

## Further reading

- https://neetcode.io/ (patterns-first interview curriculum, by Navdeep Singh)
- https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/ (complexity + patterns, by Yangshun Tay)
