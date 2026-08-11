# 3Sum — Editorial

## 1. Pattern recognition

The output is defined purely by **values** ("unique triplets", any order), not by positions — that is your license to **sort**, and sorting is what unlocks everything else. Second signal: "all pairs/triplets with a target sum" plus `n = 3000` means an O(n²) budget — enough for one loop *around* a linear scan, not for three nested loops. If you've done Two Sum II, this problem is literally that scan wearing an outer loop.

## 2. Brute force first

Three nested loops, collecting `sorted` triplets into a set to dedup: O(n³) time. With `n = 3000` that is ~4.5×10⁹ triples — hopeless at a 3-second limit. A hash-set variant (fix two, look up the third) gets to O(n²) time but O(n) extra space and *still* needs the set-of-sorted-tuples dance to dedup, which is where most bugs hide. The sorted two-pointer version gets O(n²) time, O(1) extra space, and dedup falls out of the order for free.

## 3. The key insight

**After sorting, fix the smallest element `nums[i]` and the rest is exactly Two Sum II on the suffix — and because equal values are now adjacent, "skip equal neighbors" is a complete deduplication strategy.**

## 4. Step-by-step derivation

1. Sort. Now every triplet we emit will be in non-decreasing order, so duplicates can only arise from *equal values sitting next to each other* — never from far-apart rearrangements. This is the whole reason no set is needed.
2. Outer loop: anchor `i` as the triplet's smallest element. The subproblem "find `lo < hi` in `nums[i+1:]` with `nums[lo] + nums[hi] == -nums[i]`" is Two Sum II, solved by the converging pointers. The safety argument carries over verbatim: when the sum is too small, `nums[lo]`'s best possible partner already failed, so `lo` is provably useless and can be discarded — that is why skipping candidates never skips an answer.
3. Dedup rule 1 (anchor): if `nums[i] == nums[i-1]`, every triplet starting with this value was already found by the previous anchor, which had a *strictly larger* suffix to search. Note the comparison is against `i-1`, not `i+1` — comparing forward would wrongly skip legitimate triplets like `[-1,-1,2]` that *use* two equal values.
4. Dedup rule 2 (pair): after recording a hit, move both pointers, then advance `lo` while `nums[lo] == nums[lo-1]`. Skipping `lo`'s duplicates alone suffices — for a fixed anchor and fixed `nums[lo]`, there is only one value `nums[hi]` can be, so `hi` duplicates can never produce a new triplet.
5. Early exit: once `nums[i] > 0`, all remaining values are positive and no zero sum exists — `break`, not `continue`.

## 5. Annotated Python solution

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        n = len(nums)
        for i in range(n - 2):
            if nums[i] > 0:                      # all remaining values positive
                break
            if i > 0 and nums[i] == nums[i - 1]: # same anchor as last time
                continue                         # (compare BACKWARD, not forward)
            lo, hi = i + 1, n - 1
            target = -nums[i]
            while lo < hi:
                s = nums[lo] + nums[hi]
                if s < target:
                    lo += 1
                elif s > target:
                    hi -= 1
                else:
                    res.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1                  # hop over duplicate second values
        return res
```

## 6. Complexity

- **Time O(n²)** — "sorting is n log n, then each of n anchors drives one linear pointer sweep."
- **Space O(1)** extra (ignoring the output and sort internals) — "just indices; dedup uses the order, not a set."

## 7. Edge-case traps

- **`[-1,-1,2]`-style triplets** — the anchor-dedup must compare `nums[i]` to `nums[i-1]`; comparing to `nums[i+1]` kills these legitimate answers. This is the off-by-one the hidden suite targets.
- **All zeros** — must yield exactly one `[0,0,0]`, not thousands; both dedup rules get exercised at once.
- **Fewer than three elements / empty input** — `range(n - 2)` handles it silently; don't add a special case.
- **Duplicate-heavy input** (e.g. `[-1,0,1]` repeated 1000 times) — correct dedup keeps the output tiny; a set-based brute force may pass on correctness but drown in time.
- **Answer using the array's extremes** (`[-10^5, 0, 10^5]`) — no overflow concern in Python, but mention it for other languages.

## 8. Reusable template

Not DP. The trainable template is **"sort, fix one, two-pointer the rest"** — it generalizes to 3Sum Closest, 4Sum (one more outer loop), and any k-Sum by recursion down to the two-pointer base case.

## 9. Interviewer follow-up

- *"3Sum Closest"* (16) — same skeleton; instead of collecting exact hits, track the sum minimizing `abs(s - target)`; dedup becomes unnecessary.
- *"4Sum / k-Sum"* — add outer anchors recursively; each level repeats the backward-comparison dedup; complexity O(n^(k−1)).
- *"Count triplets with sum < 0"* — when `s < target`, every `hi' in (lo, hi]` also works, so add `hi - lo` and advance `lo`; O(n²) with no dedup needed since positions, not values, are counted.
