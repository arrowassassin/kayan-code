# Sliding Window Maximum — Editorial

## 1. Pattern recognition

The window here is *fixed-size and given* — no invariant to discover, no shrink condition. The real question is a data-structure one: "maintain an aggregate (max) over a window under one insertion and one deletion per step". Sums are trivial under that regime (add, subtract); **max is not**, because when the maximum itself leaves the window you need to know the runner-up, and the runner-up's runner-up, and so on. That "aggregate that can't be subtracted" framing is the tell for a **monotonic deque** — the standard companion structure to sliding windows, and a favorite hard follow-up once a candidate has shown the basic template.

## 2. Brute force first

`max(nums[i:i+k])` for each of the `n - k + 1` windows: O(nk). At n = 10⁵ with k = n/2 that's ~2.5·10⁹ comparisons — the hidden stress test is built to kill exactly this (and the numbers are shaped so both an increasing and a decreasing run stress each end of any smarter structure). A heap seems like the fix — O(log k) insert, max at the top — but deletion of an *arbitrary* expired element is the catch; lazy deletion (pop stale indices when they surface at the top) rescues it at O(n log n). Worth naming as the fallback: it's easy to write correctly under pressure.

## 3. The key insight

**An element that is ≤ a newer element can never again be any window's maximum — the newer one is at least as large and expires later — so the window's "potential maximums" form a strictly decreasing sequence.**

## 4. Step-by-step derivation

1. Ask: which elements of the current window could still become the answer for *some* current-or-future window? If `nums[j] <= nums[i]` with `j < i`, then any window containing `j` from now on also contains `i` — `j` is permanently dominated. Discard it.
2. The survivors are decreasing (front = oldest = largest). New element `x`: pop dominated elements off the **back** (they're exactly the trailing ones `<= x`), then append. This is why a deque: evictions happen at the back (domination) *and* the front (expiry).
3. Expiry: store **indices**, not values. The front is stale when `dq[0] <= i - k` — with duplicate values you cannot decide expiry from values alone.
4. The answer for the window ending at `i` (once `i >= k - 1`) is `nums[dq[0]]` — the front survivor is the max by construction.
5. Amortized cost: each index is appended once and popped at most once (from one end or the other) → O(n) total, even though a single step may pop many. State that amortization explicitly in an interview; it's the part that sounds like magic until you say "every element pays for its own eviction once."
6. Detail worth defending: popping with `<=` (not `<`) is safe and keeps the deque strictly decreasing — an equal older element is dominated by the equal newer one.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq = deque()   # indices; nums[dq[0]] > nums[dq[1]] > ... (strictly)
        out = []
        for i, x in enumerate(nums):
            while dq and nums[dq[-1]] <= x:   # dominated: smaller AND older
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:                # front expired out of the window
                dq.popleft()
            if i >= k - 1:                    # first full window at i = k-1
                out.append(nums[dq[0]])
        return out
```

## 6. Complexity

- **Time O(n)** — "each index enters the deque once and leaves at most once, so all the while-loop pops across the whole run total n."
- **Space O(k)** — "the deque holds indices of one window at most, plus the output."

## 7. Edge-case traps

- **`k = 1`** — output is the array itself; the domination loop must not over-pop.
- **`k = len(nums)`** — a single window; expiry never fires.
- **Strictly decreasing input** — nothing is ever dominated; the deque grows to size k and expiry does all the work (one half of the stress test).
- **Strictly increasing input** — every element evicts the whole back; the deque stays size 1 (the other half of the stress test).
- **Duplicates** (`[2,2,2], k=2`) — storing values instead of indices breaks expiry here; the `<=` pop keeps only the newest copy, which is correct.
- **Negative numbers** — no sentinel tricks with 0 or `-1`; use indices and comparisons only.

## 8. Reusable template

Not DP. This trains the monotonic deque — "discard the dominated, answer at the front" — the same structure behind Shortest Subarray with Sum at Least K (862) and the deque-optimized sliding-window DP family.

## 9. Interviewer follow-up

- *"Minimum of each window instead?"* — flip the comparison; keep the deque increasing. Maintaining both simultaneously answers "max − min per window" (Longest Continuous Subarray With Absolute Diff ≤ Limit, 1438).
- *"Windows arrive as a stream and k can change?"* — deque logic survives growth; on shrink you may need to expire several fronts. A lazy-deletion heap is the honest general answer when windows aren't FIFO.
- *"Why not a max-heap?"* — make the trade-off crisp: heap O(n log n) with lazy deletion, deque O(n); the deque wins because it exploits the FIFO expiry order that a heap ignores.
- *"Sum ≥ target with negatives, shortest window?"* — plain two-pointer windows break on negatives; the fix is prefix sums plus *this exact* monotonic deque over prefix values (862) — the interviewer probe that ties the whole topic together.
