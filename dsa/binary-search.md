# Binary search

Created 2026-08-03 · Provenance: AI-drafted · Credits: Wikipedia (peer-reviewed article), GeeksforGeeks

## Summary

Binary search finds a target in a sorted array by halving the search space
each step: compare the middle element, discard the half the target can't be
in, repeat. Worst case O(log n) comparisons (Wikipedia, "Binary search").

```python
def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

The deeper idea (GfG): binary search works on any **monotonic predicate** —
"false false false ... true true". When the input isn't sorted but the *answer*
is ordered and monotone, you can binary-search the answer instead ("minimum
subarray size such that sum > k", the square-root / speed / capacity problems).

## Lesson

1. Sorted input or monotone predicate = candidate for O(log n) halving.
2. The classic bug is off-by-one on `lo`/`hi` bounds — pick one template and
   stick to it (GfG's `lo <= hi` + `mid = (lo+hi)//2`).
3. Python's `bisect` module implements this on sorted lists; know it exists
   even though interviewers may want the manual loop.

## Drill

Self-check: run `binary_search` on `[1, 3, 5, 7, 9]` for targets 5 (→2) and 4
(→-1). Then write the "first true" variant for a monotone predicate `f(i)` and
check it returns the first index where `f(i)` is True.

## Puzzles

- [puzzles/two-crystal-balls.md](puzzles/two-crystal-balls.md) — find the threshold floor with 2 eggs, the search-space-flip of binary search.

## Further reading

- https://en.wikipedia.org/wiki/Binary_search (peer-reviewed WikiJournal of Science version)
- https://www.geeksforgeeks.org/dsa/binary-search/
- https://www.geeksforgeeks.org/dsa/binary-search-identify-solve-and-interview-questions/ (identifying binary-search problems)
