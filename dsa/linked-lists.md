# Linked lists

Created 2026-08-03 · Provenance: AI-drafted · Credits: Tech Interview Handbook (Yangshun Tay), NeetCode

## Summary

A linked list is a chain of nodes, each holding a value and a pointer to the
next node. No contiguous memory → **no O(1) random access** (get by index is
O(n)), but insertion/deletion at a known position is O(1) pointer rewiring
(Tech Interview Handbook cheatsheet).

The four interview patterns (all O(1) space):
1. **Dummy/sentinel head** — `dummy.next = head` removes all special-casing
   for deleting/rebuilding the head; return `dummy.next`.
2. **Fast/slow pointers** — fast moves 2× slow. When fast hits the end, slow
   is at the middle; if they collide, there's a cycle (Floyd's).
3. **In-place reversal** — three pointers; *save `curr.next` before you
   overwrite it* (the one-line bug everyone hits).
4. **Two pointers with a gap** — "remove nth from end": lead pointer runs `n`
   steps ahead.

## Lesson

1. Always draw it before coding — pointer manipulation is visual.
2. The "save next, flip, advance" reversal template is the load-bearing skill;
   reversal + find-middle + merge solves most hard list problems.
3. Edge cases first: empty list, single node, two nodes, head removal.

## Drill

Self-check: implement `reverse(head)` iteratively with a dummy-free loop and
verify on `1→2→3` that it returns `3→2→1`. Then implement `has_cycle(head)`
with fast/slow pointers and check it returns True for a list whose tail points
back to node 2.

## Further reading

- https://www.techinterviewhandbook.org/algorithms/linked-list/ (cheatsheet: operations, techniques)
- https://neetcode.io/solutions/design-linked-list (dummy/sentinel + singly/doubly patterns)
- https://github.com/yangshun/tech-interview-handbook
