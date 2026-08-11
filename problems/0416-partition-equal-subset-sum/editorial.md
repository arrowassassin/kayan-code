# Partition Equal Subset Sum — Editorial

## 1. Pattern recognition

"Split a set into two equal-sum halves" *sounds* like a partitioning puzzle, but one reframe turns it into a standard: a valid split exists iff **some subset sums to exactly `total / 2`** — the complement is then forced to match. "Does any subset hit a target?" is **0/1 knapsack (feasibility flavor)**: each item used at most once, a capacity, a yes/no per reachable sum. The tells: subset selection, a numeric target, and small value bounds (`sum ≤ 20,000`) that scream "make the *sum* a table dimension."

## 2. Brute force first

Try all 2^n subsets — 2^200 ≈ 10^60, dead. The recursive form, "for each number: include it or not, tracking the running sum," still branches twice per element. But look at its state: `(index, remaining_target)`. Index ≤ 200, remaining target ≤ 10,000 → at most 2 × 10^6 distinct calls. Subset-sum is NP-hard in general, yet *pseudo-polynomial* when values are small — the exponentially many subsets collapse onto a small grid of (index, sum) pairs, and memoization exploits exactly that collapse.

## 3. The key insight

**Track the set of achievable sums, one number at a time: each number `x` maps the achievable set `S` to `S ∪ (S + x)`, and the answer is whether `total/2` lands in the final set.**

## 4. Step-by-step derivation

1. **Reframe:** if `total` is odd → `False` immediately. Else set `target = total // 2` and ask: does a subset sum to `target`?
2. **Name the state.** `can(i, s)` = "using only `nums[i:]`, can we make sum `s`?" What was picked earlier doesn't matter — only the remaining target does.
3. **Say the choice out loud.** "Number `i` is in the subset or it isn't: `can(i, s) = can(i+1, s) or (x ≤ s and can(i+1, s − x))`." Base case: `can(i, 0) = True` (stop picking), `can(n, s>0) = False`.
4. **Memoize:** 2^n → O(n · target) table cells, O(1) each — the exponential-to-pseudo-polynomial collapse from section 2.
5. **Compress to one row.** Row `i` reads only row `i+1`, so keep a single boolean array `dp[s]` = "achievable using numbers processed so far." The subtlety that interviews probe: update `s` from high to low. Downward, `dp[s − x]` still reflects the state *before* `x` was offered — upward, `x` could chain onto itself and you'd silently solve the unbounded-coins variant.
6. **The set-of-sums / bitset view** — worth mentioning out loud: represent achievable sums as a Python `set` (`sums |= {s + x for s in sums}`) or, slicker, as bits of one integer: `bits |= bits << x`, answer `(bits >> target) & 1`. The bitset does 10,000 boolean ORs per number in a couple of machine-word operations per 64 sums — the same DP, vectorized. Great "how would you make this fast in practice" material.

## 5. Annotated Python solution

```python
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:                    # odd total: provably impossible
            return False
        target = total // 2
        dp = [False] * (target + 1)      # dp[s] = sum s achievable so far
        dp[0] = True                     # the empty subset
        for x in nums:
            for s in range(target, x - 1, -1):   # downward: use x at most once
                if dp[s - x]:
                    dp[s] = True
            if dp[target]:               # early exit once the target is hit
                return True
        return dp[target]
```

## 6. Complexity

- **Time O(n · total)** — "for each of n numbers we sweep the sum axis once; pseudo-polynomial: polynomial in the *value* of the sum, not its bit-length." Here ≤ 200 × 10,000 = 2 × 10^6 steps.
- **Space O(total)** — "one boolean per candidate sum; the 2-D table compresses to a single row." (Bitset variant: one integer of `target` bits.)

## 7. Edge-case traps

- **Odd total** → `False` before any DP; skipping this check and flooring `total/2` accepts wrong splits.
- **Single element** → `False` — one group would be empty (sum 0 vs. a positive number).
- **The upward-sweep bug:** iterating `s` ascending reuses the same element repeatedly — `[1, 5]` would claim 2, 3, ... are achievable. This is *the* classic 0/1-knapsack implementation error.
- **`dp[0] = True`** — without the empty-subset seed, nothing is ever achievable.
- **Element larger than `target`** — must simply never be placed (the `range` bound handles it); it does *not* make the answer `False` by itself.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion):**

```python
from functools import lru_cache

class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False

        @lru_cache(maxsize=None)
        def can(i: int, s: int) -> bool:     # make sum s from nums[i:]?
            if s == 0:
                return True                  # base: target hit
            if i == len(nums) or s < 0:
                return False                 # base: out of items / overshot
            #      skip nums[i]      or  put it in the subset
            return can(i + 1, s) or can(i + 1, s - nums[i])

        return can(0, total // 2)
```

**Bottom-up (iterative table)** — the uncompressed 2-D form; section 5 is its one-row compression:

```python
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        n = len(nums)
        # dp[i][s] = can nums[i:] make sum s
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = True                  # init = base case s == 0
        for i in range(n - 1, -1, -1):       # loop order: reverse of recursion
            x = nums[i]
            for s in range(1, target + 1):
                dp[i][s] = dp[i + 1][s] or (x <= s and dp[i + 1][s - x])
        return dp[0][target]
```

**The mechanical conversion recipe:**

1. **State → params → table index.** Memo key `(i, s)` becomes the 2-D index `dp[i][s]`.
2. **Memo → table.** `@lru_cache` becomes an `(n+1) × (target+1)` boolean grid — note the extra `i = n` row for the "out of items" state.
3. **Recursion order → loop order.** `can(i, ·)` calls `can(i+1, ·)`, so the loop runs `i = n−1 .. 0` — the reverse of the recursion's descent, guaranteeing row `i+1` is complete first.
4. **Base case → initialization.** `s == 0 → True` becomes the pre-set first column; the all-`False` fill covers `i == n, s > 0`.

Final pass: row `i` depends only on row `i+1` → one rolling row with the *downward* sum sweep (section 5) — the sweep direction is doing the job the second row did.

## 9. Interviewer follow-up

- **"Minimize the difference between the two groups"** (Last Stone Weight II, 1049): same achievable-sums table; instead of testing `target`, scan for the achievable `s ≤ total/2` closest to it — answer `total − 2s`.
- **"Split into k equal groups"** (698): the sum trick alone no longer suffices; you need bitmask-over-elements DP or backtracking with pruning — good discussion of why this problem's collapse doesn't generalize.
- **"Count the subsets hitting the target / assign +/− signs"** (Target Sum, 494): booleans become counts — `dp[s] += dp[s − x]`, same downward sweep.
- **"Values up to 10^9?"** Pseudo-polynomial dies; say so — this is the moment to note subset-sum is NP-hard and pivot to meet-in-the-middle, O(2^(n/2)).
