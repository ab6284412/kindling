# Hashing

Created 2026-08-03 · Provenance: AI-drafted · Credits: Navdeep Singh (NeetCode), Python docs

## Summary

A hash map trades space for time: average O(1) insert and lookup. Python:
`dict` (key → value, insertion-ordered) and `set` (keys only). The classic
interview pattern is a *frequency counter* or *seen-set* to replace an O(n²)
scan with two O(n) passes:

```python
def has_duplicates(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

## Lesson

1. Reaching for nested loops? Ask: "can a `set`/`dict` remember what I've
   already seen?" — that's the hashing pattern.
2. `dict.get(key, default)` avoids the double lookup; `collections.Counter`
   builds frequency maps in one line.
3. Words like "contains", "duplicate", "complement", "frequency" are the
   interview's way of saying *hashing pattern*.
4. Ordering: use a `list` when order matters, a `set` for membership.

## Drill

Self-check: write `two_sum(nums, target)` returning the indices of two values
that add to `target`. Your solution must run in O(n) time. Test:
`two_sum([2, 7, 11, 15], 9)` → `(0, 1)`.

## Puzzles

- [puzzles/single-number.md](puzzles/single-number.md) — the XOR trick, hashing's pure-membership case.

## Further reading

- https://docs.python.org/3/library/stdtypes.html#mapping-types-dict (dict)
- https://docs.python.org/3/library/collections.html#collections.Counter (Counter)
