# Two pointers

Created 2026-08-03 · Provenance: AI-drafted · Credits: Navdeep Singh (NeetCode), Yangshun Tay (Tech Interview Handbook)

## Summary

On a sorted array, one left and one right pointer sweep inward, taking O(1)
space and O(n) time where a nested loop is O(n²). The classic:

```python
def two_sum_sorted(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return (lo, hi)
        if s < target:
            lo += 1
        else:
            hi -= 1
    return None
```

Why it works: sorted means moving `lo` up grows the sum, moving `hi` down
shrinks it — so every step eliminates one whole row/column of candidates.

## Lesson

1. "Sorted" is the trigger word. Unsorted input → sort first (n log n) or use
   hashing.
2. Variants: palindrome check (start=end), container-with-most-water, removing
   duplicates in place.
3. Say the invariant out loud: "left points at the smallest untried candidate,
   right at the largest."

## Drill

Self-check: write `is_palindrome` (from arrays-strings) and `two_sum_sorted`
above with the same two-pointer shape. Both must be O(n) time, O(1) space.

## Further reading

- https://neetcode.io/roadmap (two pointers section, by Navdeep Singh)
- https://www.techinterviewhandbook.org/algorithms/array/ (two-pointer + sliding-window techniques, by Yangshun Tay)
