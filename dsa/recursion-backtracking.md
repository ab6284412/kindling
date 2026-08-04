# Recursion and backtracking

Created 2026-08-03 · Provenance: AI-drafted · Credits: GeeksforGeeks

## Summary

**Recursion**: a function that calls itself on a smaller instance. Requires a
base case (where it stops) and a recursive case (reduce toward the base).

**Backtracking**: recursion plus *undo*. Build a solution incrementally; when
a partial choice can't lead to a valid answer, backtrack and try the next
option (GfG, "Backtracking Algorithm"). The template:

```python
def subsets(nums):
    out = []
    def dfs(i, path):
        if i == len(nums):
            out.append(path[:])   # copy! path is reused
            return
        dfs(i + 1, path + [nums[i]])  # take
        dfs(i + 1, path)              # skip
    dfs(0, [])
    return out
```

Worst case is exponential — O(b^d) where b is the branching factor and d the
depth — so **pruning** (rejecting dead ends early, e.g. N-Queens' is_safe,
Sudoku validity checks) is what makes it tractable (GfG).

## Lesson

1. "Generate all combinations/permutations/subsets", "is there any way to",
   constraint puzzles (N-Queens, Sudoku, maze) → backtracking.
2. The classic bug: appending a mutable `path` by reference. Append `path[:]`.
3. Know when NOT to use it: if greedy or DP solves it, backtracking is overkill.

## Drill

Self-check: run `subsets([1, 2])` → `[[1, 2], [1], [2], []]` (4 subsets).
Then write `permute([1, 2, 3])` and verify it returns 6 permutations.

## Puzzles

- [puzzles/bridge-and-torch.md](puzzles/bridge-and-torch.md) — model all valid crossings; recursion/backtracking over states.

## Further reading

- https://www.geeksforgeeks.org/dsa/backtracking-algorithms/
- https://www.geeksforgeeks.org/dsa/backtracking-algorithm-in-python/
- https://www.geeksforgeeks.org/dsa/what-is-the-difference-between-backtracking-and-recursion/
