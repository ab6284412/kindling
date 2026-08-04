# Two crystal balls

Provenance: AI-drafted · Credits: classic interview puzzle

Part of: the binary-search pattern — see [dsa/binary-search.md](../binary-search.md)

## Question

You have two crystal balls and a 100-story building. A ball breaks if dropped
from the *true breaking floor* or higher; it survives below it. Find the exact
breaking floor using the fewest worst-case drops. With one ball you'd linear-
scan from floor 1. With two, how do you beat that?

## Approach

Binary search with one ball is wrong — the first break leaves you unable to
continue (the second ball must then linear-scan, and if you used big jumps the
linear scan is long). Instead: use the first ball in *increasing* jumps to
bracket the floor, then the second ball linear-scans the bracket. Balance the
two phases by making every bracket the same size → jump by decreasing steps:
100, then 99, 98... i.e. the classic "square-root" staircase.

## Answer

Jump by `√n` (≈10): drop ball 1 at 10, 20, 30... until it breaks; then linear-
scan the 10-floor window below with ball 2. Worst case ≈ 10 + 10 = 20 drops,
O(√n). Optimal strategy is the descending staircase (100, then +99, +98...)
giving a max of ~14, but √n is the interview answer that shows you understood
the trade.

Self-check: explain in one sentence why binary search breaks the first ball
and strands you.
