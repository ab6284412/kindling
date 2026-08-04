# Graphs

Created 2026-08-03 · Provenance: AI-drafted · Credits: Tech Interview Handbook (Yangshun Tay), GeeksforGeeks

## Summary

A graph is nodes (vertices) + edges. Represent it as an **adjacency list** — a
dict `{node: [neighbors]}` — which is space-efficient (O(V + E)) and the
default in interviews (Tech Interview Handbook cheatsheet).

Two fundamental traversals:
- **BFS** (queue): visits level by level. Use it for shortest path / minimum
  steps in an *unweighted* graph, and for detecting cycles. The visited set is
  mandatory — a cyclic graph will otherwise loop forever.
- **DFS** (stack or recursion): visits as deep as possible. Use it for
  reachability, connected components, topological sort, and puzzles like
  "does a path exist".

The decision rule (GfG): **DFS or BFS?** — if the problem asks for *shortest*
path / closest / minimum steps → BFS; if it asks *whether anything exists* or
*explore everything* → DFS.

Grid problems (islands, flood fill) are just graphs where each cell's
neighbors are the four adjacent cells; track visited by mutating the grid or a
set.

## Lesson

1. Convert the problem to nodes/edges first — "islands" is "count connected
   components of '1' cells".
2. Always add to `visited` when you *enqueue/push*, not when you pop — adding
   at pop time re-enqueues duplicates and can blow up exponentially.
3. Complexity is O(V + E) time and O(V) space — say it, interviewers ask.

## Drill

Self-check: BFS on the adjacency list `{0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}`
from node 0 → visit order `[0, 1, 2, 3]` with a visited set (note the self-loop
on 3). Then count islands on `[["1","1","0"],["0","1","0"],["0","0","1"]]` → 2.

## Further reading

- https://www.techinterviewhandbook.org/algorithms/graph/ (adjacency list, BFS, DFS)
- https://www.geeksforgeeks.org/dsa/when-to-use-dfs-or-bfs-to-solve-a-graph-problem/
- https://www.geeksforgeeks.org/dsa/graph-data-structure-and-algorithms/
