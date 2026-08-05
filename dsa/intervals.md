# Intervals

Created 2026-08-05 · Provenance: AI-drafted · Credits: Yangshun Tay (Tech Interview Handbook), Navdeep Singh (NeetCode)

## Summary

Interval problems hand you ranges — `[start, end]` — and ask for merges,
overlaps, insertions, or free-gap counts (meeting rooms, calendar overlap,
merge intervals). The near-universal first move is **sort by start time, then
sweep once**: sorting turns "which ranges overlap" into "compare each interval
to the one open range I'm building" — O(n log n) for the sort, then O(n) for
the sweep.

Overlap test: `[a, b]` and `[c, d]` overlap iff `c <= b` (the next one starts
before the current one ends). A merge is `(a, max(b, d))`.

## Template / approach (merge intervals)

```python
def merge(intervals):
    intervals.sort()                  # sort by start; ties break by end
    out = []
    for lo, hi in intervals:
        if not out or lo > out[-1][1]:    # disjoint from the open range
            out.append([lo, hi])
        else:                             # overlaps: extend it
            out[-1][1] = max(out[-1][1], hi)
    return out
```

Complexity: O(n log n) time (the sort dominates the O(n) sweep), O(n) space for
the output.

## Lesson (when to use)

1. Trigger words: "merge/insert intervals", "meeting rooms / non-overlapping",
   "minimum arrows to burst balloons", "free time between bookings".
2. Sort by start first — the sweep is only correct on sorted input; most
   interview difficulty here is forgetting that one line.
3. Insert intervals = find the first range whose end `>= new.start`, merge
   everything that overlaps it, splice the rest unchanged — still O(n) after
   the search.
4. Tight overlap semantics matter: does `[1,4]` + `[4,5]` count as overlapping?
   Read the problem (the classic answer uses `c <= b`, but "no overlap on
   endpoints" is sometimes specified).

## Drill

Self-check: implement `merge` above and verify
`merge([[1,3],[2,6],[8,10],[15,18]])` → `[[1,6],[8,10],[15,18]]` and
`merge([[1,4],[4,5]])` → `[[1,5]]` (touching endpoints merge). Then implement
`insert(intervals, new)` and verify
`insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8])` →
`[[1,2],[3,10],[12,16]]`.

## Further reading

- https://neetcode.io/roadmap (intervals section, by Navdeep Singh)
- https://www.techinterviewhandbook.org/algorithms/array/ (interval techniques, by Yangshun Tay)
- https://neetcode.io/practice/practice/neetcode150 (Intervals section)
- https://en.wikipedia.org/wiki/Interval_scheduling (scheduling problems on intervals)
