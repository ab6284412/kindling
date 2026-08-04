# Dynamic programming

Created 2026-08-03 · Provenance: AI-drafted · Credits: Tech Interview Handbook (Yangshun Tay), GeeksforGeeks

## Summary

Dynamic programming (DP) is **recursion plus a cache**. A problem is DP-able
when it has two properties (GfG, "Introduction to Dynamic Programming"):
- **Overlapping subproblems** — the same subproblem is solved many times; the
  cache turns each into O(1).
- **Optimal substructure** — the optimal answer composes from optimal answers
  to smaller subproblems.

Two styles:
- **Memoization (top-down)**: keep the recursive code, add a cache keyed by
  the function arguments. Python makes this a one-liner with
  `functools.lru_cache`.
- **Tabulation (bottom-up)**: fill a table from the base case upward; avoids
  recursion depth limits.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

Without the cache, `fib(n)` calls itself ~2^n times; with it, O(n). That gap —
exponential to linear for one decorator — is the whole selling point.

The interview recipe (Tech Interview Handbook): 1) define the state (what
parameters fully describe a subproblem); 2) define the recurrence; 3) define
the base case. Classic problems: coin change, climbing stairs, house robber,
0/1 knapsack, longest common subsequence.

## Lesson

1. "Minimum/maximum/many ways to reach", overlapping subproblems → DP.
2. State = function signature. If two calls have the same arguments and the
   same remaining decision space, the answer is identical — that's the cache
   key.
3. When a memoized recursion overflows the stack, convert to bottom-up.

## Drill

Self-check: with `@lru_cache`, `fib(50)` returns in microseconds; comment out
the decorator and confirm `fib(35)` alone gets slow. Then implement
`climb(n)` (ways to climb n stairs in 1-or-2 steps) and verify
`climb(4)` → `5`.

## Further reading

- https://www.techinterviewhandbook.org/algorithms/dynamic-programming/
- https://www.geeksforgeeks.org/dsa/dynamic-programming/
- https://www.geeksforgeeks.org/dsa/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/
- https://docs.python.org/3/library/functools.html (functools.lru_cache)
