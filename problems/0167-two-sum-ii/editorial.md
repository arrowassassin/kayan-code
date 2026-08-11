# Two Sum II — Input Array Is Sorted — Editorial

## 1. Pattern recognition

Two words in the statement do all the work: **sorted** and **O(1) space**. Classic Two Sum needs a hash map precisely because the input is unordered — the map is a substitute for order. When the interviewer hands you order for free and then bans the map, they are steering you to the converging **two-pointer** scan. Rule of thumb worth saying out loud: *sorted input + "find a pair with some property of their sum" = pointers at both ends*. This is the warmup for 3Sum, where the same scan runs inside an outer loop.

## 2. Brute force first

Check every pair: `O(n^2)` time, O(1) space. With `n = 10^5` that is up to ~5×10⁹ pair checks — dead at a 3-second limit. The hash-map single pass is O(n) time but O(n) space, which the statement explicitly forbids. So we need O(n)-ish time with constant space, and sortedness is the only asset we have not spent yet.

## 3. The key insight

**With pointers at both ends of a sorted array, comparing their sum to the target tells you which pointer is *provably useless* — you discard one candidate per step, never the answer.**

## 4. Step-by-step derivation

1. Start `lo = 0`, `hi = n - 1`, and look at `s = numbers[lo] + numbers[hi]`.
2. If `s < target`: `numbers[hi]` is the **largest** value `numbers[lo]` can ever be paired with, and even that was too small. So `numbers[lo]` is out of the running with *every* remaining partner — not just this one. Advance `lo`. This exchange-style argument ("its best possible partner already failed") is the part interviewers push on; "move left because the sum is small" without the *why* sounds memorized.
3. If `s > target`: symmetric — `numbers[lo]` is the smallest available partner for `numbers[hi]`, and the sum still overshot, so `hi` can never appear in the answer. Retreat `hi`.
4. Each iteration permanently eliminates exactly one index, and the guaranteed pair is never the one eliminated (we only discard an index after proving no partner works for it). After at most `n - 1` steps the pointers meet at the answer.
5. Invariant form, if you prefer: *the answer pair is always inside `[lo, hi]`* — true initially, preserved by every move.

## 5. Annotated Python solution

```python
class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        lo, hi = 0, len(numbers) - 1
        while lo < hi:
            s = numbers[lo] + numbers[hi]
            if s == target:
                return [lo + 1, hi + 1]      # statement wants 1-indexed
            if s < target:
                lo += 1                      # lo's best partner failed -> lo is dead
            else:
                hi -= 1                      # hi's smallest partner overshot -> hi is dead
        return []                            # unreachable: exactly one pair guaranteed
```

## 6. Complexity

- **Time O(n)** — "the pointers only ever move toward each other, so there are at most n − 1 iterations total."
- **Space O(1)** — "two indices, nothing that grows with the input."

## 7. Edge-case traps

- **Returning 0-indexed positions** — the single most common wrong answer here; convert at the return, nowhere else.
- **Negative numbers and a negative target** — the pointer logic never mentions sign, so it just works; don't add special cases.
- **Duplicates forming the pair** (`[1,1], target 2`) — `lo < hi` (strict) already prevents reusing one element.
- **Answer at the extreme ends** (first + last element) — found on the very first comparison; make sure you check before moving.

## 8. Reusable template

Not DP. This is the canonical **converging two-pointer** template — the same loop, with an outer loop and dedup added, is the engine inside 3Sum (this problem's follow-up) and 3Sum Closest.

## 9. Interviewer follow-up

- *"Now find all unique triplets summing to zero"* — 3Sum (15), the linked extension: sort, fix the smallest element, run this exact scan on the suffix, and add duplicate-skipping.
- *"What if the array were not sorted?"* — hash map, O(n) time / O(n) space; sorting first costs O(n log n) and destroys the original indices, so you'd need to carry them.
- *"Count the pairs with sum < target"* — same pointers: when `s < target`, all of `numbers[lo+1..hi]` also work with `lo`, so add `hi - lo` and advance `lo`.
