# Minimum Size Subarray Sum — Editorial

## 1. Pattern recognition

"Shortest contiguous subarray whose sum reaches a threshold" — and the constraints shout the enabling fact: **all elements are strictly positive**. Positivity makes the window sum monotone in the window's extent (grow → sum rises, shrink → sum falls), and monotonicity is the license every sliding window runs on. This problem is the cleanest place to learn that the license is *conditional*: the identical statement with negatives allowed is a different problem requiring different tools, and interviewers use exactly that switch as a probe.

## 2. Brute force first

All O(n²) subarrays with a running sum per start (or O(n²) pairs over a prefix array): at n = 10⁵ that's ~5·10⁹ additions — far past a 3-second Python budget, and the hidden all-ones stress test (target = n) is built so the inner loop never exits early. The redundancy: consecutive starts re-add nearly the same elements. Keep one running sum and move both ends instead.

## 3. The key insight

**With positive elements, once the window's sum reaches `target`, growing it further is pointless — every shorter candidate ending later will be found by shrinking from the left first.**

## 4. Step-by-step derivation

1. Slide `right` across the array, keeping `window_sum` for `[left, right]`.
2. When `window_sum >= target`, the window is valid — but we want the *shortest* valid window, so a valid window should be tightened, not extended. Shrink from the left while validity holds, recording `right - left + 1` at each shrink step (harvest-while-valid, the minimization phase of the template — same shape as Minimum Window Substring, with a sum instead of character counts).
3. Why is it safe to shrink permanently? Positivity: dropping `nums[left]` decreases the sum, and if `[left, right]` fell below target, then `[left, r']` for any future `r' > right` might become valid again — but `left` never needs to move *backwards*, because any window starting before the current `left` and ending at `r'` is a superset of one we already measured, hence no shorter. Both pointers advance monotonically → O(n).
4. If the sum never reaches target, return 0 — keep `best` as infinity-sentinel and translate at the end.
5. The alternative worth naming: build prefix sums (strictly increasing, again thanks to positivity) and for each start binary-search the first prefix reaching `prefix[i] + target` — O(n log n). Strictly worse here, but it's the version that survives harder variants, so mention it.

## 5. Annotated Python solution

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        best = float("inf")
        window_sum = 0
        left = 0
        for right, x in enumerate(nums):
            window_sum += x
            while window_sum >= target:          # valid -> tighten
                best = min(best, right - left + 1)
                window_sum -= nums[left]         # positivity: sum strictly falls
                left += 1
        return 0 if best == float("inf") else best
```

## 6. Complexity

- **Time O(n)** — "each index is added to the window once and removed at most once; both pointers only move forward."
- **Space O(1)** — "a running sum and two indices."
- Binary-search alternative: **O(n log n)** time, O(n) space for the prefix array.

## 7. Edge-case traps

- **No qualifying subarray** (total sum < target) → 0, not infinity and not n.
- **Single element ≥ target** → 1; the shrink loop must be able to empty the window down to size 1 (and conceptually to 0 — the `while` handles it).
- **`>=` vs `>`** — the threshold is "at least", not "more than"; off-by-one here flips several hidden cases.
- **Whole array is the answer** (`target = 15, [1,2,3,4,5]`) — harvest must happen before the shrink invalidates.
- **Large target with small elements** — sums up to 10⁹; irrelevant in Python, an int-overflow remark worth making for other languages.

## 8. Reusable template

Not DP. This trains the sum-threshold minimization window — expand, then shrink-and-harvest while valid — plus the judgment call of when the window is *licensed* (positive elements) versus when it isn't.

## 9. Interviewer follow-up

- *"Now allow negative numbers."* — the probe this problem exists for. Shrinking is no longer justified (removing a negative *raises* the sum) and prefix sums are no longer monotone, so plain binary search dies too. Shortest subarray with sum ≥ K becomes LeetCode 862: prefix sums + a monotonic deque. Being able to say precisely *which* assumption broke — monotonicity of the window sum — is the answer they're listening for.
- *"Sum exactly equal to target?"* — with positives the same window works (check `==` at the boundary); with negatives it's prefix-sum + hash map (560-style).
- *"Count the valid subarrays instead of minimizing"* — for each `right`, once the tightest valid `left` is known, all starts ≤ that left work: add `left` (count of valid starts) per step; the window doubles as a counter.
- *"Return the subarray itself"* — track `(best_left, best_len)` at harvest time; one extra line.
