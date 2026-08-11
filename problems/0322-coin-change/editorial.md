# Coin Change — Editorial

## 1. Pattern recognition

"Fewest number of X to reach exactly Y, unlimited reuse allowed" is the **unbounded knapsack / shortest-path-on-amounts** shape. Two clues point at DP: greedy visibly fails (Example 3 is designed to show you `[1,3,4]`, `amount 6`), and the answer for an amount is built from answers for *strictly smaller* amounts — an optimal substructure you can state in one sentence. You can also see it as BFS on the graph whose nodes are amounts and whose edges subtract a coin; DP is that BFS with the layers flattened into a table.

## 2. Brute force first

Try every multiset of coins: recursively branch on each denomination at each step. The recursion `fewest(a) = 1 + min(fewest(a - c))` has branching factor up to 12 and depth up to `amount`, so the raw call tree is exponential — with `amount = 10^4` and small coins it is astronomically large. But count the *distinct* subproblems: one per amount `0..10^4`. The brute force is only slow because it re-answers the same question exponentially many times.

## 3. The key insight

**Every optimal combination has a last coin `c`; removing it must leave an optimal combination for `amount − c` — so `dp[a] = 1 + min(dp[a − c])` over all coins, and there are only `amount + 1` subproblems.**

## 4. Step-by-step derivation

1. **Name the state.** `fewest(a)` = minimum coins summing exactly to `a`. The remaining amount is the *only* thing the future needs — how you got there is irrelevant. That "forgetting is safe" property is what makes the state valid.
2. **Say the choice out loud.** "The combination for `a` ends in *some* coin. I don't know which, so I try each `c` and pay 1 plus whatever `a − c` costs." Recurrence: `fewest(a) = 1 + min over c ≤ a of fewest(a − c)`.
3. **Justify optimality (the cut-and-paste argument):** if the remainder after removing the last coin weren't optimal for `a − c`, substituting a better one would improve the whole — contradiction.
4. **Base case:** `fewest(0) = 0`. **Unreachable amounts** need a value that loses every `min` — use the sentinel `amount + 1` (no exact combination ever uses more than `amount` coins, since the smallest coin is ≥ 1).
5. **Memoize:** exponential tree → `O(amount)` distinct calls × `O(len(coins))` work each. Exponential becomes `O(amount · k)` purely by caching.
6. Bottom-up, that cache is an array filled left to right — every `dp[a − c]` is already final when `dp[a]` asks for it.

## 5. Annotated Python solution

```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        INF = amount + 1                      # sentinel: more coins than any exact answer
        dp = [0] + [INF] * amount             # dp[a] = fewest coins summing to a
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1     # last coin c + optimal rest
        return dp[amount] if dp[amount] != INF else -1
```

## 6. Complexity

- **Time O(amount × k)** where `k = len(coins)` — "one table cell per amount, each cell tries every coin once." At 10^4 × 12 that's ~10^5 operations.
- **Space O(amount)** — "one integer per reachable amount."

## 7. Edge-case traps

- **`amount = 0`** → `0`, not `-1`; the base case must be answered before any coin is considered.
- **Unreachable amounts** (`[2]`, `3`) → `-1`; forgetting the sentinel check returns garbage.
- **Coins larger than `amount`** (even `2^31 − 1`) — the `c <= a` guard must skip them, and using `float('inf')` vs. `amount + 1` both work, but the sentinel must never win a `min` *and then* be returned as a real answer.
- **Greedy traps:** `[1,3,4]`, `6` and `[186,419,83,408]`, `6249` — largest-first is wrong; the hidden suite includes both.
- **Duplicated denominations** — harmless for correctness, but dedup if you mention micro-optimizing.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion)** — the recurrence verbatim:

```python
from functools import lru_cache

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        INF = amount + 1

        @lru_cache(maxsize=None)
        def fewest(a: int) -> int:            # fewest coins summing exactly to a
            if a == 0:
                return 0                      # base case
            best = INF
            for c in coins:
                if c <= a:
                    best = min(best, fewest(a - c) + 1)
            return best

        ans = fewest(amount)
        return ans if ans != INF else -1
```

(Note: at `amount = 10^4` with coin 1 the recursion is 10^4 deep — near Python's default limit. That practical fragility is one honest reason to prefer bottom-up here.)

**Bottom-up (iterative table)** — section 5 above. **The mechanical conversion recipe:**

1. **State → params → table index.** The single memo key `a` becomes the array index: `fewest(a)` → `dp[a]`.
2. **Memo → table.** `@lru_cache` becomes `dp = [...] * (amount + 1)` — an array sized by the state space.
3. **Recursion order → loop order.** `fewest(a)` depends on smaller amounts only, so the loop runs `a = 1 .. amount` ascending — each right-hand side is filled before it's read.
4. **Base case → initialization.** `if a == 0: return 0` becomes `dp[0] = 0`; the "not yet computed" cache-miss state becomes the sentinel `INF` fill.

## 9. Interviewer follow-up

- **Count the number of combinations instead** (Coin Change II, 518): swap `min` for `+`, and — the subtle part — put the coin loop *outside* the amount loop so each combination is counted once, not once per ordering.
- **Return the actual coins:** store, per amount, which coin achieved the min (`parent[a] = c`), then walk `amount → amount − c → ...` back to 0.
- **Huge `amount`, few coins?** The table is linear in `amount`; mention BFS from 0 with early exit at `amount` (same worst case, often faster in practice), or number-theoretic tricks (Chicken McNugget) for two coins.
