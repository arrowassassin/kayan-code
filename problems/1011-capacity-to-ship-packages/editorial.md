# Capacity to Ship Packages Within D Days — Editorial

## 1. Pattern recognition

"Return the **minimum** capacity such that the job finishes within `days`" — a min-threshold question where bigger capacity can only help. Same signature as Koko Eating Bananas (this problem's warmup): binary search on the answer, with one twist. Koko's piles were independent, so her predicate was pure arithmetic. Here the packages must stay **in belt order**, so the predicate becomes a **greedy contiguous-partition simulation** — the version of the template you'll actually reuse most, because "process these in order under a budget" is how real scheduling questions are phrased.

## 2. Brute force first

Try capacities one by one from `max(weights)` upward, simulating the loading for each until one fits in `days`. The simulation is O(n), but the answer can be as large as `sum(weights)` — up to `2.5 × 10^7` here — so the scan can cost ~`10^12` operations. Even the smarter-looking alternative, trying every possible *partition* into `days` blocks, is exponential. The linear scan does hand you the predicate, though; the only thing wrong with it is how you walk the answer space.

## 3. The key insight

**Feasibility is monotonic in capacity — if capacity `c` ships everything in `days`, so does `c + 1` — so binary search the answer, not the array; the check is a greedy one-pass load simulation.**

## 4. Step-by-step derivation

1. **Predicate.** `days_needed(cap)`: walk the belt in order, keep a running load, and start a new day the moment the next package would exceed `cap`. Feasible iff `days_needed(cap) <= days`.
2. **Why greedy is correct.** Within a fixed capacity, deferring a package that *fits today* to tomorrow can never reduce the day count — tomorrow starts with strictly less remaining room for what follows. So "pack until overflow" computes the true minimum days for that capacity, in O(n). (This exchange argument is the one sentence interviewers probe; have it ready.)
3. **Monotonicity.** A day-by-day schedule that works at capacity `c` is still legal, load for load, at `c + 1`. Feasible capacities form a suffix of the number line: `F F F T T T`. Spoken out loud: *"if capacity c works, c+1 works — so I binary search the answer space."*
4. **Bounds.** `lo = max(weights)` — anything smaller can't lift the heaviest package at all, so don't start at 1 and waste iterations on capacities that are infeasible for a trivial reason. `hi = sum(weights)` — one day ships everything. Both bounds are *answers to degenerate inputs*, which is a good sanity check that they're tight.
5. **Bisect for the leftmost feasible value**: `feasible(mid)` → `hi = mid`; else `lo = mid + 1`; return when `lo == hi`.

## 5. Annotated Python solution

```python
class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        def days_needed(cap: int) -> int:
            d, load = 1, 0                 # day 1 exists even for one package
            for w in weights:
                if load + w > cap:         # would overflow -> ship, new day
                    d += 1
                    load = 0
                load += w                  # w always fits now: cap >= max(weights)
            return d

        lo, hi = max(weights), sum(weights)   # tight, provably-bracketing bounds
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid                   # keep mid: answer is mid or smaller
            else:
                lo = mid + 1               # discard mid: answer strictly larger
        return lo
```

## 6. Complexity

- **Time O(n log S)** where `S = sum(weights)` — "roughly 25 greedy simulations, each one pass down the belt."
- **Space O(1)** — "two bounds and a running load; nothing scales with input size."

## 7. Edge-case traps

- **`days == len(weights)`** — one package per day; the answer is exactly `max(weights)`, i.e. the search must be able to return `lo` untouched.
- **`days == 1`** — the answer is `sum(weights)`; the search must be able to return `hi`.
- **One giant package among tiny ones** (`[500,1,1,1,1,1], days = 2`) — the answer is pinned by the max, not by an even split of the sum; starting `lo` at 1 hides this but wastes work, starting the *greedy* wrong (allowing a package to overflow its day) breaks it.
- **Order matters** — `[10,50,10,50,10,50], days = 2` answers 110, not the 90 an "even halves" intuition suggests; contiguity forbids rebalancing.
- **Off-by-one in the greedy** — incrementing the day *after* adding the overflowing package undercounts; ship first, then load.

## 8. Reusable template

Not DP. This is the second rep of the **binary-search-on-the-answer template** from Koko (875) — the new muscle is the greedy contiguous-partition predicate, reused unchanged in Split Array Largest Sum (410).

## 9. Interviewer follow-up

- *"Now minimize the largest day-load given exactly `k` days"* — that's the linked extension, Split Array Largest Sum (410): the identical search and predicate, just inverted phrasing (capacity ↔ largest sum).
- *"Two ships loading in parallel from the same belt?"* — the greedy check breaks (assignment choices appear); discuss why the predicate now needs its own search or DP, while the outer binary search survives untouched.
- *"Capacity is fixed; how many days?"* — no search, just run the predicate once. Recognizing which side of the problem is the unknown is the whole game.
- *"Weights arrive as a stream?"* — the greedy check is already one-pass and O(1) space, so a fixed candidate capacity can be validated online; finding the *minimum* still needs the offline bounds.
