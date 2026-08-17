# Koko Eating Bananas — Editorial

## 1. Pattern recognition

"Return the **smallest** speed such that a condition holds" — the answer is a single number, not an index into the input, and the condition gets *easier* as the number grows. That combination is the signature of **binary search on the answer**: instead of searching a sorted array, you search the space of candidate answers, using a feasibility check as your comparator. This problem is the cleanest possible anchor for the framework, which is why it's a Google (and general FAANG) staple — the interviewer wants to hear you *name* the monotonic structure, not just code a loop.

## 2. Brute force first

Try every speed `k = 1, 2, 3, ...` and return the first one whose total hours fit in `h`. Each check is O(n), and the first feasible `k` can be as large as `max(piles) = 10^9` (five piles, five hours). That's up to `10^9 × 5·10^4` pile visits — dead on arrival. The brute force isn't wasted, though: it hands you the exact predicate you're about to binary search over.

## 3. The key insight

**The answer space is monotonic — if speed `k` finishes in time, every speed `k+1, k+2, ...` also finishes — so you can binary search the answer itself instead of scanning it.**

## 4. Step-by-step derivation

This is the three-step framework worth memorizing, spoken aloud in an interview:

1. **Define the predicate.** `feasible(k)` = "at speed `k`, total hours `sum(ceil(p/k)) <= h`". Computable in O(n). Ceiling division in integers: `(p + k - 1) // k`.
2. **Argue monotonicity.** Raising `k` can only shrink each `ceil(p/k)`, so total hours are non-increasing in `k`. The answer space therefore looks like `F F F F T T T T` — a block of infeasible speeds followed by a block of feasible ones. Say it out loud: *"if speed k works, k+1 works — so I binary search the answer, not the array."* That one sentence is what converts the linear scan into a log.
3. **Bracket and bisect.** Lowest sensible speed is `1`; `max(piles)` always works (every pile clears in one hour, and `h >= len(piles)` is guaranteed). Binary search for the leftmost `T`: if `feasible(mid)`, the answer is `mid` or smaller (`hi = mid`); otherwise it's strictly larger (`lo = mid + 1`). The `lo < hi` / `hi = mid` shape never discards a feasible candidate and always shrinks the range, so it terminates with `lo == hi` sitting on the boundary.

Note what we did *not* do: we never sorted `piles`, and the input order never mattered. The sortedness lives in the answer space, not the data.

## 5. Annotated Python solution

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def hours_at(k: int) -> int:
            # ceil(p / k) per pile; integer form avoids float error at 1e9
            return sum((p + k - 1) // k for p in piles)

        lo, hi = 1, max(piles)          # lo may be infeasible; hi always feasible
        while lo < hi:
            mid = (lo + hi) // 2
            if hours_at(mid) <= h:
                hi = mid                # mid works -> answer is mid or smaller
            else:
                lo = mid + 1            # mid too slow -> answer strictly larger
        return lo                       # lo == hi == leftmost feasible speed
```

## 6. Complexity

- **Time O(n log M)** where `M = max(piles)` — "about 30 feasibility checks, each a single O(n) pass."
- **Space O(1)** — "just the two search bounds; the predicate streams over the piles."

## 7. Edge-case traps

- **`h == len(piles)`** — zero slack; the answer is exactly `max(piles)`, i.e. the search terminates at `hi`. Off-by-one bugs (`hi = mid - 1`) surface here.
- **Single huge pile with tight `h`** (`[10^9], h = 10^9 - 1`) — answer is 2, not 1; ceiling division must be exact.
- **Very generous `h`** — answer collapses to 1; the loop must handle `lo` already feasible.
- **Float `math.ceil(p / k)`** — at `p = 10^9` double rounding can miscount an hour; use integer `(p + k - 1) // k` or `-(-p // k)`.
- **Overflow mindset** — hours can sum to ~`5·10^13`; fine in Python, but say so for C++/Java.

## 8. Reusable template

Not DP. This trains the **binary-search-on-the-answer template** — monotonic predicate + leftmost-true bisect — reused verbatim by Ship Packages (1011) and Split Array Largest Sum (410).

## 9. Interviewer follow-up

- *"Ship packages within D days instead"* — that's the linked follow-up, 1011: same template, but the predicate becomes a greedy contiguous-partition check (order now matters).
- *"Minimize hours for a given speed instead?"* — no search needed; that's just evaluating the predicate once.
- *"What if Koko can split an hour across piles?"* — total hours become `ceil(sum(piles)/k)`; the answer is a closed form `ceil(sum/h)`, no search at all. Recognizing when monotonic structure degenerates to arithmetic is a nice flex.
- *"Fractional speeds allowed?"* — binary search over reals with a tolerance, or note the optimal real speed is determined by the same predicate; the framework carries over unchanged.
