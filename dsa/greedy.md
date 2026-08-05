# Greedy algorithms

Created 2026-08-05 · Provenance: AI-drafted · Credits: Yangshun Tay (Tech Interview Handbook), Wikipedia contributors

## Summary

Greedy means: at each step take the locally optimal choice and never look back
— no exploring of alternatives, no undoing. It is correct only when **local
optimality implies global optimality** (the greedy choice property) and the
problem has **optimal substructure** (an optimal solution contains optimal
solutions to its subproblems). Where it applies it is usually the fastest
correct answer — O(n log n) after a sort, versus exponential backtracking.

The sanity-check intuition is the **exchange argument**: assume an optimal
solution differs from the greedy one at some step, and argue you can swap the
optimal choice for the greedy choice without making the answer worse; then,
step by step, greedy matches an optimal solution. You won't write this out in
an interview — you use it to decide whether greedy is safe at all.

## Template / approach (interval scheduling — max non-overlapping jobs)

```python
def schedule(jobs):                 # jobs = [(start, end), ...]
    jobs.sort(key=lambda x: x[1])   # greedy: earliest-finish first
    taken, last_end = [], -1
    for s, e in jobs:
        if s >= last_end:
            taken.append((s, e))
            last_end = e
    return taken
```

Why earliest-finish works: finishing earliest leaves the most room left, and
the exchange argument shows no optimal solution can do better. Complexity:
O(n log n) for the sort, O(n) scan, O(n) space.

## Lesson (when to use / when greedy fails)

1. Trigger words: "minimum number of coins/arrows/jumps", "maximize the number
   of non-overlapping", "task scheduling", "gas station" — then always ask:
   "could a locally-best choice lock me out of a better global answer?"
2. **When greedy fails** — coin change with arbitrary denominations (coins
   {1, 3, 4}: greedy gives 4+1+1 for 6, but 3+3 is better), 0/1 knapsack
   (fractional knapsack is greedy-friendly; 0/1 is not). The counterexample
   mindset: before committing, try to build a small case where the greedy step
   is wrong — if you find one, reach for DP.
3. Greedy is often the "is this the easy version?" check — if greedy holds the
   problem is simple; if you keep finding counterexamples, it is DP.

## Drill

Self-check: implement `schedule` above and verify it returns 4 jobs for
`[(1,3),(2,4),(3,6),(5,7),(6,8),(8,9)]` → `[(1,3),(3,6),(6,8),(8,9)]`. Then
prove the failure mode to yourself: for coins {1, 3, 4} greedy reaches 6 as
4+1+1 (3 coins) while 3+3 uses 2 — greedy is not globally optimal there.

## Further reading

- https://en.wikipedia.org/wiki/Greedy_algorithm (greedy choice property)
- https://neetcode.io/roadmap (greedy section, by Navdeep Singh)
- https://neetcode.io/practice/practice/neetcode150 (Greedy section)
