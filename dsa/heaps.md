# Heaps / priority queues

Created 2026-08-03 · Provenance: AI-drafted · Credits: Python docs (heapq), GeeksforGeeks

## Summary

A heap is a binary tree stored in an array where every parent is ≤ its
children (min-heap), so the root `heap[0]` is always the smallest element
(Python docs, `heapq`). Python ships it as the `heapq` module:

- `heappush`, `heappop`: O(log n)
- `heap[0]`: peek smallest, O(1)
- `heapify(list)`: turn a list into a heap, O(n)
- `nlargest`/`nsmallest`: top-K without sorting everything
- Max-heap: store negated values (GfG)

Why it matters in interviews: the **Top-K pattern**. "Kth largest element" /
"merge K sorted lists" / "find median of a stream" are all solved by keeping a
heap of size K (O(n log k)) instead of sorting (O(n log n)) (Python docs
priority-queue notes; NeetCode "Heap / Priority Queue" section).

## Lesson

1. "K largest/smallest/frequent", "always need the current min/max" → heap.
2. `heapq` is a min-heap; for a max-heap push `-x` and negate on pop.
3. Interview gotcha: `heapq` is not thread-safe and has no direct "find item
   by value" — the docs' add/remove/mark-Removed recipe is the pattern for
   mutable priority queues.

## Drill

Self-check: `heap = []; heapq.heappush(heap, 5); heapq.heappush(heap, 1);
heapq.heappush(heap, 3)` then `heapq.heappop(heap)` → `1`. Then implement
`kth_largest(k, nums)` with a min-heap of size k and verify
`kth_largest(3, [3, 2, 1, 5, 6, 4])` → `4`.

## Further reading

- https://docs.python.org/3/library/heapq.html (heapq: heap queue algorithm)
- https://www.geeksforgeeks.org/python/heap-and-priority-queue-using-heapq-module-in-python/
- https://neetcode.io/practice/practice/neetcode150 (Heap / Priority Queue section)
