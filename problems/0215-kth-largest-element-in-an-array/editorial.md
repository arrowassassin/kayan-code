# Kth Largest Element in an Array — Editorial

## 1. Pattern recognition

"Find the k-th largest / smallest / closest / most frequent" is the signature of the **Top-K pattern**. The tell in the statement is that you're asked for a *rank*, not a full ordering — and the explicit nudge "can you do better than sorting?" confirms the interviewer wants the k-vs-n conversation. This problem is the canonical entry point: master it and Top-K Frequent Elements (its linked follow-up), K Closest Points, and every "stream of scores, keep the leaders" question fall out of the same template.

## 2. Brute force first

Sort descending, return `nums[k-1]`: O(n log n) time, one line. It passes here — 10⁵ elements sort in milliseconds — so the constraint doesn't kill it; the *question* does. Sorting computes the rank of every element when you were asked for one. Saying "sorting works in n log n, but I can do n log k with a heap, or expected O(n) with quickselect" is the expected opening, and choosing between those two is the real interview content.

## 3. The key insight

**You never need the order of all n elements — a min-heap of size k always holds the k largest seen so far, and its root *is* the k-th largest.**

## 4. Step-by-step derivation

1. Keep a pool of the k best candidates while scanning. A new element matters only if it beats the *weakest* member of the pool — so the pool must expose its minimum cheaply. That is a **min-heap** (yes, a min-heap for a "largest" problem — the counterintuitive half of the pattern).
2. Heapify the first k elements: O(k), not O(k log k) — `heapq.heapify` is linear, a fact worth saying out loud.
3. For each remaining element, if it exceeds the root, `heapreplace` (pop + push in one sift): O(log k). Total O(n log k), space O(k). When k ≪ n this crushes sorting; when k ≈ n, it *is* heapsort, so no worse.
4. **Quickselect** takes a different deal: partition around a random pivot as in quicksort, but recurse only into the side containing index `n-k`. The recursion touches n + n/2 + n/4 + … ≈ 2n elements → **O(n) average**, O(1) extra space, but **O(n²) worst case** if pivots keep landing badly (random pivots make that vanishingly unlikely; deterministic median-of-medians guarantees O(n) but nobody codes it live).
5. The interview script: lead with the heap (safe, streaming-friendly, easy to write correctly), then *offer* quickselect for the average-case-linear bragging right. If the interviewer says "the data arrives as a stream" or "memory is tiny", the heap is the only answer — quickselect needs the whole array in hand and mutates it.
6. Python shortcut to mention, not to hide behind: `heapq.nlargest(k, nums)[-1]` implements exactly this heap loop.

## 5. Annotated Python solution

```python
import heapq


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        # Min-heap of the k largest values seen so far.
        # Python's heapq is ALWAYS a min-heap — which is exactly
        # what we want here: the root is the weakest keeper.
        heap = nums[:k]
        heapq.heapify(heap)                 # O(k), linear — not k log k
        for x in nums[k:]:
            if x > heap[0]:                 # beats the current weakest?
                heapq.heapreplace(heap, x)  # pop root + push, one sift
        return heap[0]                      # root = k-th largest overall
```

Quickselect, the average-O(n) alternative:

```python
import random


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        target = len(nums) - k              # index in ascending order

        def select(lo, hi):
            pivot = nums[random.randint(lo, hi)]   # random pivot: expected O(n)
            lt, i, gt = lo, lo, hi
            while i <= gt:                  # 3-way partition survives duplicates
                if nums[i] < pivot:
                    nums[lt], nums[i] = nums[i], nums[lt]
                    lt += 1; i += 1
                elif nums[i] > pivot:
                    nums[i], nums[gt] = nums[gt], nums[i]
                    gt -= 1
                else:
                    i += 1
            if target < lt:  return select(lo, lt - 1)
            if target > gt:  return select(gt + 1, hi)
            return pivot                    # target lands in the == band

        return select(0, len(nums) - 1)
```

## 6. Complexity

- Heap: **Time O(n log k)**, **Space O(k)** — "each of n elements does at most one log-k sift into a heap that never exceeds k entries."
- Quickselect: **Time O(n) average, O(n²) worst**, **Space O(1)** ignoring recursion — "each partition halves the expected work, so n + n/2 + n/4 + … is a geometric 2n."

## 7. Edge-case traps

- **`k == len(nums)`** — the answer is the minimum; the heap loop's `nums[k:]` is empty and must fall through cleanly.
- **All duplicates** (`[7,7,7,7]`) — a 2-way quickselect partition can go quadratic here; the 3-way (Dutch flag) partition above is the fix.
- **Negative numbers** — anyone "negating for a max-heap" elsewhere must not confuse themselves here; the min-heap needs no negation.
- **k = 1 / single element** — degenerate but must work.
- Off-by-one converting "k-th largest" to the ascending index `n - k`.

## 8. Reusable template

Not DP. This trains the **bounded min-heap for top-k** template — the same k-sized-heap-plus-one-pass loop reappears in Top-K Frequent Elements, K Closest Points, and Merge K Sorted Lists.

## 9. Interviewer follow-up

- *"Now the elements arrive as a stream / don't fit in memory"* — the heap answer survives untouched (O(k) memory); quickselect dies. This is exactly Kth Largest in a Stream (703).
- *"K-th most **frequent** instead of largest?"* — count first, then run the same top-k machinery over (frequency, value) pairs: that's the linked follow-up, Top-K Frequent Elements (347).
- *"Guaranteed worst-case linear?"* — name median-of-medians as the deterministic pivot rule; say you'd use randomized quickselect in practice.
- *"Values in a small known range?"* — counting sort gives O(n + range) with no heap at all.
