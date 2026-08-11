# Kth Largest Element in a Stream — Editorial

## 1. Pattern recognition

"Report an order statistic after every stream arrival" is the **maintained top-k** pattern: a design-class wrapper around a heap. The signals: the query repeats after each update (so a from-scratch recompute wastes everything you knew a call ago), and only a *rank* is asked for, not the full order. Like every problem in this stream-design family, open by declaring the budget: construction O(n log n) at worst, then **O(log k) per `add`, O(k) space** — the state must not grow with the stream.

## 2. Brute force first

Keep every value in a list; each `add` appends and re-sorts (or re-scans with `heapq.nlargest`): O(n log n) per call, O(n) memory. With 10⁴ initial values plus 10⁴ adds, that's ~10⁴ sorts of ~10⁴ elements — order 10⁸–10⁹ work, at or past the time limit, and the memory grows with the stream, which the pattern forbids. Even keeping the list sorted and inserting with `bisect.insort` is O(n) per add for the shift — better, but still stream-length-bound.

## 3. The key insight

**To answer "k-th largest" you only need the k largest values — and stored in a MIN-heap, the smallest of those champions sits at the root, and that root IS the answer.**

## 4. Step-by-step derivation

1. A value below the current k-th largest can never climb into the top k (new arrivals only push the bar *up*), so everything below rank k is permanently irrelevant — discard it. State shrinks from O(n) to O(k).
2. Now the counter-intuitive step, and the one to narrate carefully in an interview: you want a *largest*-side statistic, yet you keep a **min**-heap. Why: of the k values you kept, the one you must be able to (a) *report* and (b) *evict* is the **smallest** of them — it is simultaneously the k-th largest overall and the weakest champion. A min-heap is precisely the structure that exposes its minimum in O(1) and replaces it in O(log k). A max-heap of the same k values buries the answer at a leaf — the heap's direction follows which *end* of the kept set you touch, not which end the problem names.
3. `add(val)`: if the heap holds fewer than k values (short `nums` at construction), push unconditionally. Otherwise compare against the root: `val <= heap[0]` → ignore; `val > heap[0]` → `heapreplace` (one sift, cheaper than pop-then-push). Either way, return `heap[0]`.
4. Construction: heapify all of `nums` (O(n)), then pop down to k — or push through the `add` logic. Ties need no care: duplicates are ordinary values, and rank counts them.

## 5. Annotated Python solution

```python
import heapq


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)            # O(n), cheaper than n pushes
        while len(self.heap) > k:           # discard everything below rank k
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:         # still warming up (nums was short)
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:            # beats the weakest champion
            heapq.heapreplace(self.heap, val)   # evict + insert, one sift
        return self.heap[0]                 # root = k-th largest, by design
```

## 6. Complexity

- **Time**: construction O(n log n) worst case, then **O(log k)** per `add` — "each add is at most one sift through a heap that never exceeds k elements."
- **Space O(k)** — "we keep only the k champions; the stream's length never enters memory."

## 7. Edge-case traps

- **`nums` shorter than k** (even empty with k=1) — the heap starts under-full; `add` must push unconditionally until size k, *then* start gating on the root.
- **Duplicates** — k-th largest counts repeats ([7,7,7] with k=2 → 7); a set-based "top k distinct" is a different (wrong) problem.
- **`val` equal to the root** — must be ignored (`>` not `>=`); replacing on equality is harmless for the answer but does pointless work — say why either way.
- **Negative values / all-equal streams** — nothing special, but they catch accidental `0` sentinels.
- **Returning `heap[0]` after an ignored value** — the answer is the root even when nothing changed; don't return `val`.

## 8. (DP section — not applicable)

Not DP. The reusable template: **size-k opposite-direction heap** — min-heap for top-k-largest, max-heap for top-k-smallest; the same inversion drives Top K Frequent Elements 347 and the two-heap median (295).

## 9. Interviewer follow-up

- *"k-th smallest instead?"* — mirror everything: size-k **max**-heap (negate values in Python), evict when `val < root`.
- *"k-th largest in a sliding window / with deletions?"* — a lone heap can't delete arbitrary members; use lazy deletion with a counter map, or two heaps balanced around rank k (the Find Median from Data Stream 295 architecture — median is just k = n/2 that moves).
- *"Full median or arbitrary quantiles at scale?"* — exact answers need the two-heap or order-statistic tree; at data-warehouse scale you'd discuss sketches (t-digest) — approximate, mergeable, fixed memory.
- *"Concurrent adds?"* — a binary heap's sift touches O(log k) slots, so it needs a lock; sharding by hash and merging per-shard top-k sets on query is the scale-out answer (top-k is mergeable, which is why this pattern distributes so well).
