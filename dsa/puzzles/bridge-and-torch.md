# Bridge and torch

Provenance: AI-drafted · Credits: classic interview puzzle

Part of: the recursion/backtracking pattern — see [dsa/recursion-backtracking.md](../recursion-backtracking.md)

## Question

Four people — taking 1, 2, 5, and 10 minutes — must cross a bridge at night.
At most two cross at a time, and they carry one torch (needed for any
crossing). The pair crosses at the *slowest* member's speed. Get everyone
across in 17 minutes or less.

## Approach

Greedy "always send the two fastest" fails (gives 19). The insight: the two
slowest (5, 10) should cross *together* to pay the 10-minute cost once, not
twice. The 1-minute person ferries the torch back.

## Answer

1. 1 + 2 cross (2 min), 1 returns (1) → 3
2. 5 + 10 cross (10), 2 returns (2) → 15
3. 1 + 2 cross (2) → 17

Total 17. The trick is scheduling the two slow ones as a single trip.

Self-check: prove in one line why sending 1 alone to shuttle 5 and 10
separately takes 19, not 17.
