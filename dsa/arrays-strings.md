# Arrays and strings

Created 2026-08-03 · Provenance: AI-drafted · Credits: Yangshun Tay (Tech Interview Handbook), Navdeep Singh (NeetCode), Python docs

## Summary

Arrays are contiguous blocks of memory — O(1) index reads, O(n) insert/delete
in the middle (everything shifts). In Python, `list` is a dynamic array: it
over-allocates, so appends amortize to O(1). Strings are immutable — every
"modification" allocates a new string (an `n`-long loop doing `s += c` is
O(n²); build a `list` and `''.join()` instead).

## Lesson

1. "Can I do it with two indices moving from both ends?" → two-pointers pattern.
2. "Does order of output matter?" → sort first (n log n) or bucket/count.
3. Check bounds before indexing — Python reads from the end with negative
   indices, which silently do the wrong thing off-by-one.
4. In-place tricks (partition, swap) are the interview flex, but an extra array
   is the *safe* answer first; optimize after the brute force works.

## Drill

Self-check: write `is_palindrome(s: str) -> bool` two ways — O(n) space using
`reversed`/slicing, and O(1) space with two pointers. Both must agree on
`"racecar"` (True) and `"hello"` (False).

## Further reading

- https://docs.python.org/3/tutorial/datastructures.html (list methods)
- https://neetcode.io/roadmap (arrays & hashing section, by Navdeep Singh)
- https://www.techinterviewhandbook.org/algorithms/array/ (by Yangshun Tay)
