# Sliding window

Created 2026-08-03 · Provenance: AI-drafted · Credits: Tech Interview Handbook (Yangshun Tay), NeetCode

## Summary

For contiguous-subarray/substring problems: keep two pointers (`left`, `right`)
moving the same direction, maintain the window's aggregate state incrementally,
and slide. The state update is O(1) per step, and since each index enters the
window once and leaves at most once, the nested-looking loop is amortized O(n).

Two shapes (Tech Interview Handbook):
- **Fixed window**: length `k` is given. Add the entering element, drop the
  leaving one, record the answer each step.
- **Variable window**: length is the answer. Expand `right`; shrink `left`
  with an inner `while` when the constraint breaks (longest) or when the
  window is satisfied and you want it shorter (shortest).

```python
def longest_without_repeating(s):
    seen = set()
    left = best = 0
    for right, c in enumerate(s):
        while c in seen:          # shrink until constraint holds
            seen.remove(s[left]); left += 1
        seen.add(c)
        best = max(best, right - left + 1)
    return best
```

Canonical problems: LC 3 Longest Substring Without Repeating Characters,
LC 209 Minimum Size Subarray Sum, LC 76 Minimum Window Substring.

## Lesson

1. Trigger words: "longest substring/subarray", "at most K distinct",
   "window of length k", "minimum size ... sum".
2. Amortized O(n) is the whole point — say it: "each element enters and leaves
   the window once."
3. **Do not** use sliding window on non-contiguous subsequences (that's
   hashing/prefix-sum) or where the aggregate isn't monotone (mixed-sign sums).

## Drill

Goal: write both sliding-window shapes and prove the amortized O(n) claim by
measuring it against a nested loop.

Steps:
1. Fixed window — max sum of any length-`k` subarray. Write
   `max_sum_fixed(a, k)`: sum the first `k`, then slide (add `a[i]`, drop
   `a[i-k]`), tracking the max. No nested loop.
2. Variable window — `longest_unique(s)`: longest substring with no repeating
   character, using a `set` and a `while`-shrink loop (the template in
   `dsa/sliding-window.md`).
3. Prove the amortization. Time `longest_unique` against a brute-force
   `for i in range(n): for j in range(i, n)` version on a 10_000-char string
   (`time.perf_counter`). The brute force must be at least ~100× slower.
4. Add asserts at the bottom and run the file — it must print nothing and exit 0.

```python
from time import perf_counter
import random, string

def max_sum_fixed(a, k):
    cur = sum(a[:k])
    best = cur
    for i in range(k, len(a)):
        cur += a[i] - a[i - k]
        best = max(best, cur)
    return best

def longest_unique(s):
    seen = set(); left = best = 0
    for right, c in enumerate(s):
        while c in seen:
            seen.remove(s[left]); left += 1
        seen.add(c)
        best = max(best, right - left + 1)
    return best

assert max_sum_fixed([2, 1, 5, 1, 3, 2], 3) == 9
assert max_sum_fixed([1, 4, 2, 10, 23, 3, 1, 0, 20], 4) == 39
assert longest_unique("abcabcbb") == 3
assert longest_unique("bbbbb") == 1

n = 10_000
s = "".join(random.choices(string.ascii_lowercase, k=n))
t0 = perf_counter(); longest_unique(s); t1 = perf_counter()
t0 = perf_counter()
for i in range(n):
    for j in range(i + 1, n):
        pass  # count work without building substrings
t2 = perf_counter()
print(f"window {t1 - t0:.4f}s vs brute {t2 - t1:.4f}s")
```

Self-check (pass/fail):
- The four asserts hold.
- The printed window time is at least ~100× smaller than the nested-loop time
  (it should be: O(n) vs O(n²)).
- You can state the invariant in one sentence: each index enters the window
  once and leaves once, so the total work is linear even though the code reads
  as two nested loops.

Why this matters: subarray problems are the most common "easy-sounding, easy-to-
get-wrong" interview class, and the amortized-O(n) argument is the thing
interviewers probe after you code it.

## Further reading

- https://www.techinterviewhandbook.org/algorithms/array/ (sliding-window technique section)
- https://github.com/yangshun/tech-interview-handbook (maintained by Yangshun Tay)
- https://neetcode.io/practice/practice/neetcode150 (Sliding Window section)
