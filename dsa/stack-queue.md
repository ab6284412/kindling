# Stack and queue

Created 2026-08-03 · Provenance: AI-drafted · Credits: GeeksforGeeks, Python docs

## Summary

- **Stack** (LIFO): last in, first out — like a pile of plates. Python `list`
  with `append()` / `pop()` is a perfect O(1) stack.
- **Queue** (FIFO): first in, first out — like a line. Python's list is a
  **trap** for this: `pop(0)` shifts every remaining element, so it's O(n).
  Use `collections.deque` and `popleft()` for O(1) (GfG, "Stack and Queues in
  Python").

```python
from collections import deque
q = deque([1, 2, 3])
q.append(4)          # enqueue, O(1)
q.popleft()          # dequeue, O(1)
```

Interview shapes: balanced brackets (push openers, pop on closer), undo,
monotonic stack for "next greater/smaller element" (each element pushed/popped
at most once → O(n)), and implementing a queue with two stacks (amortized
O(1): pour the inbox into the outbox only when the outbox is empty).

## Lesson

1. "Most recent first" / "undo" / "matching pairs" → stack. "First come,
   first served" / "level order" / "shortest steps" → queue (deque).
2. `pop(0)` on a list is the classic performance bug — a benchmark doubles the
   time each time you double the list (the O(n) fingerprint).
3. Thread-safety: `queue.LifoQueue`/`queue.Queue` exist but are slower; plain
   list/deque for single-threaded interview code.

## Drill

Self-check: implement `is_balanced("([{}])")` → True and
`is_balanced("([)]")` → False with a stack. Then explain in one line why
`q.popleft()` is O(1) but `list.pop(0)` is O(n).

## Further reading

- https://www.geeksforgeeks.org/python/stack-in-python/
- https://www.geeksforgeeks.org/dsa/stack-queue-python-using-module-queue/
- https://www.geeksforgeeks.org/dsa/queue-using-stacks/
