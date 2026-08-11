# House Robber — Editorial

## 1. Pattern recognition

"Pick a subset to maximize a total, but each pick disables its neighbor" — an **adjacency constraint on a line**. Whenever the payoff of a decision depends only on a small summary of what came before (here: "did I take the previous house?"), you are looking at 1-D dynamic programming. This is *the* canonical problem for practicing the DP interview loop: state the choice out loud, write the recurrence, memoize, then mechanically convert to a loop. Its follow-up, Maximum Profit in Job Scheduling (1235), is the same decision with "previous house" generalized to "latest non-conflicting job".

## 2. Brute force first

Every house is in or out: 2^n subsets, filter out the ones with adjacent picks, take the max — O(2^n). At n = 100 that is ~10^30 subsets; dead on arrival. The recursive form of the brute force, `best(i) = max(best(i+1), nums[i] + best(i+2))`, still branches twice per house — but notice it only ever asks 100 *distinct* questions. That observation is the whole trick.

## 3. The key insight

**At each house the only thing that matters about the past is the best total for the prefix ending there — so `dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])`: skip house `i`, or rob it on top of the best answer two houses back.**

## 4. Step-by-step derivation

1. **Name the state.** Let `best(i)` = maximum cash obtainable from houses `0..i-1`. One integer parameter — that's the entire "state of the world" the future needs.
2. **Say the choice at that state out loud.** House `i-1` is either skipped ("whatever `best(i-1)` was carries over") or robbed ("I bank `nums[i-1]`, and the previous house is off-limits, so I add it to `best(i-2)`"). Recurrence: `best(i) = max(best(i-1), best(i-2) + nums[i-1])`.
3. **Base cases** fall out of reading the definition at tiny inputs: `best(0) = 0` (no houses), `best(1) = nums[0]` — or even simpler, `best(0) = best(-1) = 0` and let the recurrence handle everything.
4. **Why memoization collapses the cost:** the naive recursion recomputes `best(i)` exponentially often (the call tree is the Fibonacci tree), but there are only `n+1` distinct states. Cache each answer once → O(n) total work. Exponential → linear purely by never answering the same question twice.
5. **Shrink space.** `best(i)` reads only `best(i-1)` and `best(i-2)`, so two rolling variables replace the array: O(1) space.

## 5. Annotated Python solution

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        # take = best total ending with the current house robbed
        # skip = best total with the current house not robbed
        take, skip = 0, 0
        for x in nums:
            # rob it  -> previous house must have been skipped
            # skip it -> inherit the better of the two previous states
            take, skip = skip + x, max(take, skip)
        return max(take, skip)
```

## 6. Complexity

- **Time O(n)** — "one pass, constant work per house: each state is computed exactly once."
- **Space O(1)** — "the recurrence only looks back two steps, so two variables replace the whole table."

## 7. Edge-case traps

- **Single house** — must return `nums[0]`, not 0; the rolling-variable init handles it, an off-by-one `dp` array often doesn't.
- **Two houses** — answer is `max`, never the sum.
- **Zeros everywhere** — answer 0; robbing nothing is legal.
- **`[2,1,1,2]`** — kills both greedy strategies (alternate houses; richest first). The optimal solution skips *two* houses in a row, which surprises people.
- Values up to 400 × 100 houses — sums fit easily, but in fixed-width languages mention overflow.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion)** — write the choice exactly as you said it:

```python
from functools import lru_cache

class Solution:
    def rob(self, nums: list[int]) -> int:
        @lru_cache(maxsize=None)
        def best(i: int) -> int:          # best for houses 0..i-1
            if i <= 0:                    # base case: no houses left
                return 0
            #        skip house i-1   or  rob it + best two back
            return max(best(i - 1), best(i - 2) + nums[i - 1])
        return best(len(nums))
```

**Bottom-up (iterative table)** — same recurrence, filled in dependency order:

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [0] * (n + 1)                # init = the base case
        dp[1] = nums[0] if n else 0
        for i in range(2, n + 1):         # loop order: smaller i first
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])
        return dp[n]
```

**The mechanical conversion recipe** (learn it once, apply everywhere):

1. **State → params → table index.** The memo key `i` becomes the array index: `best(i)` → `dp[i]`.
2. **Memo → table.** `@lru_cache` becomes an explicit array sized by the state space (`n+1` entries).
3. **Recursion order → loop order.** The recursion tops out at base cases and unwinds upward, so the loop runs the *opposite* way: from base cases toward the final query (`i = 2 .. n`). Rule of thumb: iterate so every value on the right-hand side is already filled.
4. **Base case → initialization.** The `if i <= 0: return 0` guard becomes `dp[0] = 0` (and `dp[1] = nums[0]`) written before the loop.

Then, as an optional final pass, notice the table is only read at offsets `-1` and `-2` and compress it to two variables — that's the solution in section 5.

## 9. Interviewer follow-up

- **The houses form a circle (House Robber II, 213):** house 0 and house n−1 are now adjacent. Run the line version twice — once excluding the first house, once excluding the last — and take the max.
- **Jobs with arbitrary start/end times and profits** — this is the linked extension, Maximum Profit in Job Scheduling (1235): "the previous house" generalizes to "the latest job ending before mine starts", found with binary search. House Robber is exactly its 1-D special case where every job has length 2 and unit spacing.
- **Return which houses to rob:** keep the `dp` array (don't compress) and walk backward — at each `i`, `dp[i] != dp[i-1]` means house `i-1` was taken; skip two, else skip one.
