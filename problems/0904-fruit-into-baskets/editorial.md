# Fruit Into Baskets — Editorial

## 1. Pattern recognition

Half the difficulty is translation: "two baskets, one type each, pick from every tree, stop at a third type" decodes to **longest contiguous subarray with at most 2 distinct values**. Practicing that decode matters — interviewers deliberately wrap window problems in stories to see if you can extract the invariant. Once decoded, the signals are textbook: longest window, a property ("≤ 2 distinct") that is monotone under shrinking, and per-element updates that are cheap with a count map. This is the friendliest member of the "at most K distinct" sub-family, and the direct warmup for Subarrays With K Different Integers (its linked follow-up), where the same window gets used as a *counting* device.

## 2. Brute force first

For every starting tree, walk right until a third type appears: O(n) starts × O(n) walk = O(n²). At n = 10⁵ that's ~10¹⁰ steps in the worst case (long two-type stretches) — far past the limit, and the hidden stress test is a 100k alternating array built to produce exactly those long walks. The waste: starts `i` and `i+1` traverse nearly identical stretches; a window reuses that traversal.

## 3. The key insight

**"At most 2 distinct types" can only be violated by the element just added, and can always be repaired by shrinking from the left — so one window pass visits each tree at most twice.**

## 4. Step-by-step derivation

1. Maintain `count`, a map from fruit type to its number of occurrences inside the window. `len(count)` is the number of distinct types.
2. Expand: `right` moves one tree per step, `count[fruits[right]] += 1`. Now `len(count)` is at most 3 — the new tree is the only possible offender.
3. Repair: while `len(count) > 2`, evict `fruits[left]`. Decrement its count and — the step people botch — **delete the key when the count reaches 0**. Leave zombie zero-count keys in place and `len(count)` overcounts, so the shrink loop never terminates believing three types remain.
4. Harvest: after repair the window is valid; record `right - left + 1`. Maximums are harvested after repair (contrast with Minimum Window Substring, which harvests *during* shrink — maximize-valid vs minimize-valid is the one structural decision in the whole template).
5. Nothing here is special about 2: replace the literal with `k` and you have the general "at most K distinct" window — worth mentioning unprompted, since the follow-up depends on it.

## 5. Annotated Python solution

```python
from collections import defaultdict


class Solution:
    def totalFruit(self, fruits: list[int]) -> int:
        count = defaultdict(int)   # type -> occurrences in window
        best = left = 0
        for right, f in enumerate(fruits):
            count[f] += 1
            while len(count) > 2:            # only the new tree can offend
                count[fruits[left]] -= 1
                if count[fruits[left]] == 0:
                    del count[fruits[left]]  # keep len(count) honest
                left += 1
            best = max(best, right - left + 1)
        return best
```

## 6. Complexity

- **Time O(n)** — "each tree enters the window once and leaves at most once; map operations are O(1)."
- **Space O(1)** — "the map never holds more than 3 types at once."

## 7. Edge-case traps

- **Zero-count zombie keys** — forgetting the `del` makes `len(count)` wrong; the single most common bug in this family.
- **Fewer than 3 distinct types overall** — the shrink loop never runs; the answer is n.
- **Single tree** → 1.
- **Best window not at the start** (`[1,2,3,2,2]` → skip tree 0) — greedy "start at index 0 and restart on failure" undercounts; the window handles it naturally.
- **Type 0 is a valid type** — don't use 0 or falsiness as a sentinel.

## 8. Reusable template

Not DP. This trains the "at most K distinct" window — count map + honest key deletion — reused verbatim in Longest Substring with At Most K Distinct Characters (340) and as the engine inside Subarrays With K Different Integers (992).

## 9. Interviewer follow-up

- *"Three baskets? K baskets?"* — change the `2` to `k`; nothing else moves. Interviewers love this because a hard-coded pair-of-variables solution (basket1/basket2) collapses here while the count-map version generalizes for free.
- *"Count the subarrays with **exactly** K distinct types"* — the linked follow-up (992): you can't window 'exactly K' directly because it isn't monotone, but `exactly(K) = atMost(K) − atMost(K−1)` runs this exact code twice.
- *"What if some trees subtract fruit (negative counts) and you want max fruit collected?"* — the window's validity is no longer monotone in length, the shrink rule loses its justification, and you pivot to prefix sums — the classic probe on *when a window is not legal*.
