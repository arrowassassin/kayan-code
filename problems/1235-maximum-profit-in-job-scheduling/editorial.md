# Maximum Profit in Job Scheduling — Editorial

## 1. Pattern recognition

★ Snowflake-reported. "Pick non-conflicting weighted things to maximize a total" is **weighted interval scheduling** — and the fastest way to recognize it is to see House Robber (198, this problem's warmup) hiding inside. In House Robber the "jobs" are houses: house `i` occupies the slot `[i, i+2)` of the street, all slots have identical shape, and "the latest compatible choice" is always mechanically `i − 2`. Here the intervals have arbitrary lengths and positions, so "the latest compatible job" must be *computed* — but the take-or-skip decision is unchanged. Two red flags rule out greedy: profits are weighted (the classic *unweighted* "activity selection" greedy — most jobs by earliest end — cheerfully picks two 20s over one 100), and `n = 5 × 10^4` with times up to 10^9 says "sort + binary search," not "make time an array index."

## 2. Brute force first

Each job is in or out: O(2^n) subsets with a conflict check — gone at n = 50,000. The structured recursion — sort jobs, then at each job "skip it, or take it and jump to the latest non-conflicting job" — has only `n` distinct states, so memoization gives a polynomial algorithm; but if the "jump" is found by scanning backward, each state pays O(n) and the total is O(n²) ≈ 2.5 × 10^9 steps — the hidden 50,000-job stress test exists precisely to kill this version. The final upgrade, binary search for the jump, is what earns the Hard tag.

## 3. The key insight

**Sort jobs by end time; then each job is either skipped, or taken on top of the best schedule ending at or before its start — and because "best profit by time t" is monotone in t, that predecessor is found by binary search: `dp[k] = max(dp[k-1], profit[k] + best_by_time(start[k]))`.**

## 4. Step-by-step derivation

1. **Recover the House Robber decision.** For each job, say the choice out loud: "take it — then I keep everything compatible that finishes by my start — or skip it." In House Robber "compatible" was `dp[i-2]` by construction. The whole derivation here is making `dp[i-2]` earn its living.
2. **Why sort by end time?** The subproblem "best profit using jobs that finish by time `t`" must be *closed*: it can't depend on jobs outside it. Sorting by end time makes every such subproblem a **prefix** of the job list — job `k`'s compatible set is exactly the jobs ending `≤ start[k]`, all of which precede it in sorted order. (Sorting by start gives the mirrored suffix formulation; end-order matches the prefix habit.)
3. **Name the state.** `dp[k]` = best profit using only the first `k` jobs (in end order). Recurrence: `dp[k] = max(dp[k-1], p_k + dp[j])` where `j` = number of jobs ending `≤ s_k`.
4. **Why memoization/tabulation is polynomial:** 2^n subsets collapse onto n prefix states — each subset's *future* depends only on the last finish time it commits to, and in end-order that is summarized by a prefix index. Exponential → O(n · cost-of-finding-j).
5. **Find `j` in O(log n).** `dp` is non-decreasing (a longer prefix never hurts), so keep the *frontier* as two parallel increasing arrays: `ends` and `best`. For each job, `bisect_right(ends, s) − 1` lands on the richest schedule finishing at or before `s` — `bisect_right`, not `bisect_left`, because a job may start the instant another ends. Append `(e, take)` only when `take` improves on `best[-1]`; skipped entries are dominated and can never be a future answer.
6. **Total:** sort O(n log n) + n binary searches O(n log n). The O(n²) backward scan dies on the stress test; this passes with two orders of magnitude to spare.

## 5. Annotated Python solution

```python
import bisect

class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int],
                      profit: list[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))   # by end time
        # Monotone frontier: ends[] increasing, best[k] = max profit
        # achievable using jobs that finish at or before ends[k].
        ends = [0]                            # sentinel: "nothing scheduled yet"
        best = [0]
        for e, s, p in jobs:
            # richest compatible prefix: last entry with end <= s
            # (bisect_right: touching at s is allowed)
            i = bisect.bisect_right(ends, s) - 1
            take = best[i] + p
            if take > best[-1]:               # record only improvements,
                ends.append(e)                # keeping both arrays increasing
                best.append(take)
        return best[-1]
```

The `if take > best[-1]` line quietly implements `max(dp[k-1], take)`: not appending *is* "skip", because the frontier already carries the best-so-far.

## 6. Complexity

- **Time O(n log n)** — "sorting dominates; then each job does one binary search into the frontier."
- **Space O(n)** — "the sorted job list plus a frontier of at most one entry per job."

## 7. Edge-case traps

- **Touching jobs must chain** — end 3 / start 3 is legal. `bisect_right` vs `bisect_left` is the single character carrying that rule; flipping it fails `[1,3,5],[3,5,7]` → 30.
- **Unweighted-greedy bait** — `[1,4,2],[3,6,10],[50,60,100]` → 110: the two short jobs beat the 100-profit one... and on Example 2 the opposite happens. Only the DP arbitrates.
- **All jobs mutually overlapping** → answer is the single max profit; the sentinel `(0, 0)` entry makes this fall out naturally.
- **Duplicate jobs / equal end times** — sorting tuples and the "improvements only" append handle both; no dedup needed.
- **Huge sparse times (up to 10^9)** — anything that allocates an array indexed by time is doomed; the frontier is indexed by *jobs*, which is the point.
- **O(n²) predecessor scan** — correct, and TLEs on the hidden 5 × 10^4 stress case by design.

## 8. Top-down AND bottom-up (+ the mechanical conversion recipe)

**Top-down (memoized recursion)** — sort by *start* time and recurse forward over suffixes ("take → jump to the next job starting at or after my end"):

```python
import bisect
from functools import lru_cache

class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int],
                      profit: list[int]) -> int:
        jobs = sorted(zip(startTime, endTime, profit))    # by start time
        starts = [s for s, _, _ in jobs]

        @lru_cache(maxsize=None)
        def suffix_best(k: int) -> int:       # best profit using jobs[k:]
            if k == len(jobs):
                return 0                      # base case: no jobs left
            s, e, p = jobs[k]
            nxt = bisect.bisect_left(starts, e)   # first job starting >= my end
            #          skip jobs[k]        or   take it and jump
            return max(suffix_best(k + 1), p + suffix_best(nxt))

        return suffix_best(0)
```

(Recursion depth can reach n = 5 × 10^4 — far past CPython's default limit. On the stress test this version needs `sys.setrecursionlimit` and luck; the iterative version needs nothing. That asymmetry is a fair interview talking point.)

**Bottom-up (iterative table)** — the same recurrence, mirrored to end-time-sorted prefixes; section 5 is this with the table compressed to the improving frontier:

```python
import bisect

class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int],
                      profit: list[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))    # by end time
        ends = [e for e, _, _ in jobs]
        n = len(jobs)
        dp = [0] * (n + 1)                    # init = base case: dp[0] = 0
        for k in range(1, n + 1):             # loop order: prefixes, ascending
            e, s, p = jobs[k - 1]
            j = bisect.bisect_right(ends, s, 0, k - 1)  # jobs ending <= s
            dp[k] = max(dp[k - 1], p + dp[j])
        return dp[n]
```

**The mechanical conversion recipe:**

1. **State → params → table index.** The memo key `k` (a position in the sorted order) becomes the array index `dp[k]`.
2. **Memo → table.** `@lru_cache` becomes `dp = [0] * (n + 1)` — one slot per state including the empty base.
3. **Recursion order → loop order.** The top-down version recurses on *larger* `k` (suffixes); flipping to prefixes reverses every dependency, so the loop ascends `1 .. n` and both `dp[k-1]` and `dp[j]` (with `j < k`) are final when read.
4. **Base case → initialization.** `if k == n: return 0` becomes `dp[0] = 0` — the sentinel "no jobs, no profit" that also absorbs the all-overlapping edge case.

**The bridge back to House Robber:** set every job to `[i, i+2)` with profit `nums[i]` and the binary search always returns `i − 1` in 0-indexed prefix terms — `dp[k] = max(dp[k-1], p + dp[k-2])`, character for character the House Robber recurrence. House Robber is the special case where compatibility is so regular that the lookup constant-folds; this problem is what remains when it doesn't. Practicing 198 → 1235 *is* practicing the generalization move interviewers reward: keep the decision, upgrade the lookup.

## 9. Interviewer follow-up

- **"Return the chosen jobs."** Keep the full `dp` array (not the compressed frontier) and backtrack from `k = n`: `dp[k] == dp[k-1]` → job skipped; otherwise it was taken — emit it and jump to its `j`.
- **"At most `k` jobs" / "two machines"** — add the budget to the state: `dp[k][used]` or `dp[k][machine-free-times]`; state design, not new machinery.
- **"Jobs arrive online / times are floats?"** Sorting handles floats untouched; for online arrival keep the frontier in a balanced-BST-like structure (`SortedList`) and insert jobs as they land, discussing when dominated entries can be pruned.
- **"What if all profits are 1?"** Now earliest-end greedy *is* optimal (activity selection) — being able to say precisely why the weights broke the greedy (an exchange argument no longer goes through) closes the loop on section 1.
