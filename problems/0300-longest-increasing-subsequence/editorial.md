# Longest Increasing Subsequence — Editorial

## 1. Pattern recognition

"Longest subsequence with property P" is a classic DP family: exponentially many subsequences, but the *best answer ending at each index* is a small, combinable summary. The tell is that whether `nums[i]` can extend a subsequence depends only on the subsequence's **last element** — everything before it is irrelevant to the future. Whenever the future only cares about a small fingerprint of the past, compress the past into that fingerprint and you have your DP state. LIS is also a rite of passage because it has a second act: a non-obvious O(n log n) upgrade interviewers love to ask for.

## 2. Brute force first

Enumerate every subsequence (2^n of them, ~10^752 at n = 2500), keep the increasing ones, take the longest. Even the smarter recursive form — "at each index, either skip it or take it if it beats the last taken value" — is O(2^n). But notice its state: `(current index, value of last taken element)`. The last value is always some `nums[j]`, so there are only O(n^2) distinct states. The exponential blow-up is pure recomputation.

## 3. The key insight

**Anchor subproblems at their last element: `dp[i]` = length of the longest increasing subsequence ending exactly at `i`, so `dp[i] = 1 + max(dp[j])` over `j < i` with `nums[j] < nums[i]`.**

## 4. Step-by-step derivation

1. **Why "ending at `i`" and not "within the first `i`"?** Because "best within a prefix" isn't extendable — you don't know its tail value. "Best ending at `i`" tells the future exactly what it needs: the tail is `nums[i]`. Choosing a state you can *extend* is half the craft of DP.
2. **Say the choice out loud:** "the subsequence ending at `i` came from some earlier `j` with a smaller value — I try them all — or `i` stands alone." `dp[i] = 1 + max({0} ∪ {dp[j] : j < i, nums[j] < nums[i]})`.
3. **Memoization / tabulation:** n states, O(n) work each → O(n^2). At n = 2500 that's ~3×10^6 comparisons — fine. Answer: `max(dp)` (the LIS can end anywhere).
4. **The O(n log n) upgrade** replaces "scan all j" with a data structure holding only what matters. Keep `tails[k]` = the smallest tail among all increasing subsequences of length `k+1` seen so far. Two facts make this fly:
   - `tails` is **always sorted**: a length-(k+1) subsequence contains a length-k one with a strictly smaller tail.
   - A new `x` improves exactly one entry: the first `tails[i] >= x` can be lowered to `x` (same length, better tail — greedily keeping tails minimal can never hurt later extensions). If no entry is ≥ `x`, `x` extends the longest subsequence: append.
   Sorted + single replacement = binary search, O(log n) per element. This is "patience sorting": dealing cards onto piles, each card on the leftmost pile whose top is ≥ it; the pile count is the LIS length.

## 5. Annotated Python solution

```python
import bisect

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        # tails[k] = smallest possible tail of an increasing
        # subsequence of length k+1; invariant: sorted.
        tails = []
        for x in nums:
            i = bisect.bisect_left(tails, x)   # first tail >= x
            if i == len(tails):
                tails.append(x)                # x extends the longest run
            else:
                tails[i] = x                   # same length, smaller tail
        return len(tails)
```

`bisect_left` (not `bisect_right`) enforces *strict* increase: an equal value replaces its twin instead of extending it — exactly why `[7,7,7,7]` yields 1.

## 6. Complexity

- **Time O(n log n)** — "each element does one binary search into a list that's at most n long." (The O(n^2) table version: "n states, each scanning all earlier states.")
- **Space O(n)** — "the tails list holds at most one entry per distinct subsequence length."

## 7. Edge-case traps

- **Duplicates** (`[7,7,7,7]` → 1, `[2,2]` → 1): the strict/non-strict distinction lives in one character (`bisect_left` vs `bisect_right`, `<` vs `<=`). Say which one you're using and why.
- **Strictly decreasing input** → 1; every element replaces `tails[0]`.
- **Single element** → 1, not 0.
- **Negative values / extremes** (`[-10^4, 10^4]`) — no special handling needed, but don't initialize with fake sentinels like 0.
- **Misconception check:** `tails` is *not* an actual LIS — only its length is meaningful. If asked to reconstruct the sequence, you need predecessor links (see section 9).

## 8. Top-down AND bottom-up (+ the conversion recipe)

Both versions below implement the O(n^2) recurrence — the form you should be able to produce mechanically before reaching for patience sorting.

**Top-down (memoized recursion):**

```python
from functools import lru_cache

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        @lru_cache(maxsize=None)
        def ending_at(i: int) -> int:          # LIS length ending exactly at i
            best = 1                           # base case: i stands alone
            for j in range(i):
                if nums[j] < nums[i]:          # j can precede i
                    best = max(best, ending_at(j) + 1)
            return best
        return max(ending_at(i) for i in range(len(nums)))
```

**Bottom-up (iterative table):**

```python
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [1] * n                           # init = the base case
        for i in range(n):                     # loop order: left to right
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

**The mechanical conversion recipe:**

1. **State → params → table index.** The memo key `i` becomes the array index: `ending_at(i)` → `dp[i]`.
2. **Memo → table.** `@lru_cache` becomes `dp = [1] * n` — one slot per state.
3. **Recursion order → loop order.** `ending_at(i)` calls only smaller indices, so iterate `i` ascending; every `dp[j]` on the right-hand side is already final.
4. **Base case → initialization.** "Standing alone = 1" moves from the `best = 1` default into the table's initial fill.

The patience-sorting version in section 5 is then a separate *algorithmic* improvement layered on top — the recipe gets you from exponential to O(n^2) mechanically; getting to O(n log n) takes the tails insight.

## 9. Interviewer follow-up

- **"Return the subsequence itself."** O(n^2) version: keep `parent[i]` = the `j` that achieved `dp[i]`, walk back from the argmax. O(n log n) version: record for each element which tails slot it landed in, then trace backward.
- **"Longest *non-decreasing* subsequence?"** Switch `bisect_left` → `bisect_right` (or `<` → `<=` in the table version). Being able to flip this on request shows you understand the invariant rather than the incantation.
- **"Number of distinct LIS?"** (673) Track a count alongside each length; combine counts when lengths tie.
- **2-D version — Russian Doll Envelopes (354):** sort by width ascending, height *descending* within equal widths, then run 1-D LIS on heights. The descending tiebreak prevents same-width envelopes from chaining — a beautiful reuse of this exact routine.
