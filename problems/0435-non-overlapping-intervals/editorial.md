# Non-overlapping Intervals — Editorial

## 1. Pattern recognition

Intervals again — but read the verb. Merge Intervals asks you to *combine*; this asks you to *select a maximum non-conflicting subset* (removing the fewest is the same thing said backwards). Selection problems are classic **greedy scheduling**, and they flip the fundamental Intervals decision: merging sorts by **start**, selection sorts by **end**. Being able to say *which* key and *why* — before writing code — is exactly what this problem tests.

## 2. Brute force first

Try every subset and check the largest conflict-free one: O(2ⁿ), dead on arrival. A smarter classic is interval-scheduling DP: sort, and let `dp[i]` = longest non-overlapping chain ending at interval `i`, giving O(n²). At n = 10⁵ that's 10¹⁰ comparisons — far past a 3-second budget. The constraint is the tell: 10⁵ demands O(n log n), i.e. sort plus a linear greedy scan.

## 3. The key insight

**Among all intervals that could be kept next, the one that ends earliest is always a safe choice — it constrains the future least, so sorting by end and greedily keeping whatever fits is optimal.**

## 4. Step-by-step derivation

1. Reframe: minimize removals ⇔ maximize the number of kept, pairwise non-overlapping intervals. Removals = n − kept.
2. Why sort by **end**, not start? The spoken justification is an exchange argument: suppose an optimal solution's first kept interval is `X`, and `E` is the interval with the earliest end overall. Swap `X` for `E`. Since `E` ends no later than `X`, everything that fit after `X` still fits after `E` — the solution stays valid and the same size. So "always keep the earliest finisher" loses nothing. Sorting by start has no such guarantee: a huge `[1,100]` can start first and block everything (greedy-by-start keeps 1 where 3 were possible on `[[1,100],[2,3],[4,5]]`).
3. Scan the end-sorted list with one variable, `kept_end`. For each `[s, e]`: if `s >= kept_end`, keep it and set `kept_end = e`; else it collides with a kept interval that finishes no later, so removing *this* one is the safe choice — count it.
4. Note the endpoint convention: here touching is **allowed**, so the test is `s >= kept_end`. It is the opposite of Merge Intervals' convention — state yours out loud at the clarify gate, and know that flipping `>=` to `>` is the one-character difference.
5. When you skip an interval you never update `kept_end` — the kept interval's earlier end keeps future options maximal.

## 5. Annotated Python solution

```python
class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        # Sort by END: the earliest finisher is always safe to keep.
        intervals.sort(key=lambda it: it[1])

        removed = 0
        kept_end = float("-inf")
        for start, end in intervals:
            if start >= kept_end:      # >= : touching does NOT conflict here
                kept_end = end         # keep it; it finishes earliest among survivors
            else:
                removed += 1           # conflict -> drop the later-finishing one
        return removed
```

## 6. Complexity

- **Time O(n log n)** — "the sort dominates; the greedy scan is a single pass with O(1) work per interval."
- **Space O(1)** auxiliary — "just a counter and the last kept end (ignoring sort internals)."

## 7. Edge-case traps

- **Touching intervals** `[1,2],[2,3]` → 0 removals; writing `>` instead of `>=` wrongly removes one. The convention is inverted from Merge Intervals — the pair of problems is designed to catch pattern-matching on autopilot.
- **All duplicates** `[0,5]×4` → keep exactly one, remove 3.
- **A giant interval covering many small ones** `[[1,10],[2,3],[4,5],[6,7]]` → remove the giant (1), not the three small ones; sort-by-start greedy gets this wrong.
- **Negative coordinates** — seed `kept_end` with `-inf`, not `0`.
- **Single interval** → 0.
- **Long overlapping chain** (the stress test) — every interval overlaps its neighbor; greedy keeps every other one.

## 8. (DP section — not applicable)

Not DP (though the O(n²) chain DP is the honest stepping stone). This trains the reusable **sort-by-end greedy selection** template — the same argument powers activity selection, minimum arrows to burst balloons, and maximum non-overlapping meetings.

## 9. Interviewer follow-up

- *"Instead of dropping conflicts, how many rooms would it take to run them all concurrently?"* — that is Meeting Rooms II 253, the linked follow-up: keep a min-heap of active end times, or sweep +1/−1 events, and report the peak.
- *"Return which intervals to remove, not just the count"* — same scan; record the skipped ones.
- *"Weighted intervals — maximize total kept weight"* — greedy breaks; you need sort + binary search + DP (Maximum Profit in Job Scheduling 1235).
- *"Prove the greedy"* — deliver the exchange argument from section 4 in two sentences; interviewers frequently ask for it verbatim.
