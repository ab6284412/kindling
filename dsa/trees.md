# Trees

Created 2026-08-03 · Provenance: AI-drafted · Credits: Tech Interview Handbook (Yangshun Tay), GeeksforGeeks

## Summary

A binary tree is a hierarchy where each node has at most two children
(GfG, "Binary Tree Data Structure"). A **binary search tree (BST)** adds the
ordering invariant: every node's left subtree holds smaller values, its right
subtree larger — which makes search O(log n) on a balanced tree (Tech
Interview Handbook).

Three DFS traversal orders plus level-order:
- **Pre-order**: root, left, right (used to serialize/copy a tree).
- **In-order**: left, root, right — on a BST this yields sorted order; it's
  the canonical way to validate a BST.
- **Post-order**: left, right, root (used to delete / compute bottom-up
  answers like height, diameter).
- **Level-order (BFS)**: a queue, level by level (min depth, right-side view).

Recursion is the default for trees: if a subtree's answer composes into the
whole answer, recurse. Space is O(h) (balanced → O(log n); skewed tree is a
linked list → O(n)).

## Lesson

1. Ask the interviewer: binary tree or BST? The answer changes the algorithm.
2. Most tree problems = pick the traversal + decide whether information flows
   top-down (path sums, validate BST) or bottom-up (height, diameter).
3. Learn the recursive traversals cold, then write them iteratively (stack for
   DFS, deque for BFS).

## Drill

Self-check: implement `inorder(root)` and confirm it returns `[1, 2, 3, 4]`
for the tree `2` with children `1` and `3` (+ right child `4`). Then implement
`is_bst(root)` using the in-order-sorted test and verify it rejects a tree
where a right subtree contains a smaller value.

## Further reading

- https://www.techinterviewhandbook.org/algorithms/tree/ (binary trees, BST, traversal)
- https://www.geeksforgeeks.org/dsa/binary-tree-data-structure/
- https://www.geeksforgeeks.org/dsa/introduction-to-binary-tree/
