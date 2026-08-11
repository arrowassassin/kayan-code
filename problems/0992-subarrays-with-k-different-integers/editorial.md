# Subarrays with K Different Integers — Editorial

## 1. Pattern recognition

"Count subarrays with **exactly** K distinct" looks like one more sliding-window rep after Fruit Into Baskets (its linked warmup) — until you try it. A window works when the property is *monotone*: growing can only break it, shrinking can only fix it (or vice versa). "Exactly K distinct" is neither — a window at exactly K might need to grow (adding a duplicate keeps K) *and* might need to shrink for other candidates. Recognizing a **non-monotone property** and knowing the standard repair — express it as a difference of two monotone ones — is the entire lesson, and it's a favorite interviewer probe precisely because pattern-matching on the warmup walks you into the wall.

## 2. Brute force first

Enumerate every start, extend right while tracking a set, add 1 whenever the set size equals k, stop past k: O(n²). At n = 2·10⁴ that's ~2·10⁸ window extensions with hashing inside — over a 3-second Python budget, and the hidden 20k alternating stress case is tuned so it fails while the linear solution finishes in milliseconds. It's also worth noticing *why* it feels wasteful: neighboring starts re-scan almost the same elements.

## 3. The key insight

**exactly(K) = atMost(K) − atMost(K−1): "exactly K distinct" isn't window-able, but it is the difference of two properties that are.**

## 4. Step-by-step derivation

1. "At most K distinct" is monotone under shrinking, so the standard template applies: expand `right`, shrink while `len(count) > K` (deleting zero-count keys so `len` stays honest — the Fruit Into Baskets bug, still here).
2. Turn that window into a *counter*. After repair, `[left, right]` is the widest valid window ending at `right`, and validity is closed under shrinking from the left — so **every** start in `[left, right]` gives a valid subarray ending at `right`. That's `right − left + 1` subarrays, summed per step. This "add the window length each step" move is the general recipe for counting subarrays under a monotone property.
3. Inclusion–exclusion on the answer: every subarray with at most K distinct has either exactly ≤ K−1 or exactly K, so `atMost(K) − atMost(K−1)` counts exactly-K subarrays, each exactly once. No clever windowing of "exactly" required — subtraction does it.
4. `atMost(0)` must return 0 (an empty count map can never admit any element); the code's shrink loop handles it naturally since `len(count) > 0` triggers on every element.
5. Two O(n) passes → O(n) total. (The one-pass three-pointer variant exists — two lefts, one right — worth *mentioning*, rarely worth writing under time pressure.)

## 5. Annotated Python solution

```python
from collections import defaultdict


class Solution:
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
        def at_most(k: int) -> int:
            count = defaultdict(int)
            left = total = 0
            for right, x in enumerate(nums):
                count[x] += 1
                while len(count) > k:            # monotone -> shrinkable
                    count[nums[left]] -= 1
                    if count[nums[left]] == 0:
                        del count[nums[left]]    # keep len(count) honest
                    left += 1
                total += right - left + 1        # all valid starts for this right
            return total

        return at_most(k) - at_most(k - 1)       # exactly K by subtraction
```

## 6. Complexity

- **Time O(n)** — "two linear window passes; in each, both pointers only move forward."
- **Space O(k)** — "the count map holds at most k+1 keys at any moment."

## 7. Edge-case traps

- **`k` equal to the total number of distinct values** — only full-coverage subarrays count (`[1,2,3,4], k=4` → 1); off-by-one in the subtraction shows up here.
- **`k = 1`** — `at_most(0)` must be 0, not crash; runs of equal values contribute triangular numbers (`[1,1,1]` → 6).
- **Duplicates around a lone value** (`[2,2,1,2,2,3], k=2`) — counting `right − left + 1` (not 1) per step is what makes each subarray counted exactly once.
- **Zombie zero-count keys** — inherited trap from the warmup; `len(count)` lies without the `del`.
- **Large counts** — answers reach ~n²/2 ≈ 2·10⁸; fine in Python, a real overflow concern in fixed-width languages (say it in the interview).

## 8. Reusable template

Not DP. This trains two composable moves: "sum of window lengths counts subarrays under a monotone property," and "exactly-K = atMost(K) − atMost(K−1)" — the pair transfers wholesale to Binary Subarrays With Sum (930) and Count Subarrays With Score / bounded-max variants.

## 9. Interviewer follow-up

- *"Longest subarray with exactly K distinct?"* — different question, different fix: run at-most-K and only harvest lengths when `len(count) == k`; the subtraction trick is for *counting*, not optimizing — articulating that distinction is the point of the question.
- *"Exactly K odd numbers instead of K distinct?"* — same subtraction (Count Number of Nice Subarrays, 1248), or map odd→1/even→0 and count prefix sums; shows the template is about monotone predicates, not "distinct" specifically.
- *"Subarrays with sum exactly S, negatives allowed?"* — at-most windows die entirely (no monotonicity with negatives); the answer is prefix-sum + hash-map counting — the classic "when can't a window work?" probe.
- *"One pass instead of two?"* — the three-pointer variant: maintain `left1` (widest at-most-K) and `left2` (widest at-most-(K−1)) against one `right`; add `left2 − left1` per step.
