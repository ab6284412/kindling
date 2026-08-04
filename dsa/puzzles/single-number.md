# Single number

Provenance: AI-drafted · Credits: classic bit-manipulation interview question

Part of: the hashing pattern's pure-membership case — see [dsa/hashing.md](../hashing.md)

## Question

Every integer in the list appears exactly twice except one, which appears
once. Find it in O(n) time and O(1) extra space.

## Approach

A `set` works but uses O(n) space. The O(1) trick: XOR. `x ^ x = 0`, `x ^ 0 = x`,
and XOR is commutative — so XORing the whole list pairs everything off to zero
and leaves only the singleton.

```python
def single_number(nums):
    acc = 0
    for x in nums:
        acc ^= x
    return acc
```

## Answer

`[2, 2, 1]` → `2 ^ 2 ^ 1 = 0 ^ 1 = 1`. Returns `1`. This is the gateway to
bit-manipulation problems (counting bits, missing numbers).

Self-check: run the function on `[4, 1, 2, 1, 2]` by hand — the answer is `4`.
