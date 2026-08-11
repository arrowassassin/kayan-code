# Find Median from Data Stream — Editorial

## 1. Pattern recognition

"Numbers arrive one at a time" + "query an order statistic at any moment" is the **streaming order-statistic** pattern, and its canonical instrument is **two heaps balanced against each other**. The give-away is that the median only ever depends on the *boundary* between the lower and upper halves of the data — you never need the halves internally ordered, just their facing extremes. Whenever a design question asks you to maintain "the middle" (median, percentile, k-th element) under inserts, this is the pattern to reach for; it extends Merge K Sorted Lists (this problem's warmup) from "heap as dispatcher over static sorted sources" to "heaps as a self-balancing partition of a live stream".

## 2. Brute force first

Option A: append to a list, sort inside `findMedian` — O(n log n) per query. Option B, the smarter naive: keep the list sorted with `bisect.insort` — the *search* is O(log n) but the insertion shifts O(n) elements, so `addNum` is O(n). With 4·10⁴ adds that's ~8·10⁸ element moves in the worst case — the stress test punishes it, and more importantly the statement explicitly prices `addNum` at O(log n), so an interviewer will stop you at the requirement. The lesson to voice: a sorted array gives cheap *reads* but expensive *writes*; the median needs cheap both.

## 3. The key insight

**Split the stream into a max-heap of the smaller half and a min-heap of the larger half — the median is always read off the two roots, and inserts only need O(log n) rebalancing.**

## 4. Step-by-step derivation

1. The median touches at most two values: the largest of the lower half and the smallest of the upper half. So maintain exactly those halves and expose exactly those two elements.
2. "Largest of a set, cheap insert" → max-heap (`lo`). "Smallest of a set, cheap insert" → min-heap (`hi`). Python's `heapq` is min-only, so `lo` stores **negated** values — the standard idiom, worth stating out loud before writing it.
3. Two invariants make the structure correct:
   - **Ordering**: every value in `lo` ≤ every value in `hi`.
   - **Size**: `len(lo) - len(hi)` is 0 or 1 (`lo` owns the middle element when n is odd).
4. The slick insert avoids case analysis entirely: push the new number into `lo`; then pop `lo`'s max and push it into `hi` (this *forces* the ordering invariant, regardless of where the new number belonged); then, if `hi` outgrew `lo`, move `hi`'s min back. Three heap operations, no branches on the number's value — much harder to get wrong live than the "compare against both roots" version.
5. `findMedian`: odd count → `lo`'s root; even count → average of the two roots. O(1).
6. Each `addNum` is a constant number of O(log n) sifts → **O(log n) insert, O(1) query, O(n) space**.

## 5. Annotated Python solution

```python
import heapq


class MedianFinder:
    """lo = max-heap (negated) of the smaller half,
    hi = min-heap of the larger half.
    Invariants: max(lo) <= min(hi); len(lo) - len(hi) in {0, 1}."""

    def __init__(self):
        self.lo = []                # negated values: heapq is min-only
        self.hi = []

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        # Force the ordering invariant: lo's max crosses to hi.
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Restore the size invariant: lo owns the odd element.
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])           # odd count: middle lives in lo
        return (-self.lo[0] + self.hi[0]) / 2.0  # even: average the facing roots
```

## 6. Complexity

- **Time O(log n)** per `addNum`, **O(1)** per `findMedian` — "each insert is at most three heap sifts; the median is literally the two roots."
- **Space O(n)** — "every number lives in exactly one of the two heaps."

## 7. Edge-case traps

- **Forgetting to negate (or un-negate) `lo` values** — the max-heap-by-negation idiom fails silently: medians drift wrong only on asymmetric streams, which is why the descending-insert test (5,4,3,2,1) exists.
- **Sorted-order arrivals** (ascending or descending) — naive "push to whichever side looks right" implementations without rebalancing degenerate to one giant heap and a wrong median.
- **Duplicates straddling the middle** (`[2,2,2,2]`) — the ordering invariant is ≤, not <; both heaps may hold equal values.
- **Even/odd alternation** — off-by-one in the size invariant shows up as medians lagging one insert behind.
- **Integer division** — `(a + b) / 2` must be float division; `//` passes the odd cases and fails the even ones.

## 8. Reusable template

Not DP. This trains the **two-heap balanced partition** — the go-to structure for streaming medians, percentile trackers, and "sliding window median" (480), where the same invariants meet lazy deletion.

## 9. Interviewer follow-up

- *"99% of numbers are in [0, 100]"* — swap the heaps for a fixed-size count array plus two overflow buckets; median by prefix-count walk, O(1)-ish per op. The heap answer is general; the counting answer exploits the distribution — say both.
- *"Sliding window median (remove old numbers)?"* — heaps can't delete arbitrary elements cheaply; add lazy deletion with a tombstone map, or switch to two multisets / an order-statistics tree (LC 480).
- *"Arbitrary percentile, not just the 50th?"* — same two heaps with the size invariant set to the p : (1−p) ratio.
- *"Distributed stream, approximate is fine?"* — exact medians don't merge across shards; name t-digest / Greenwald–Khanna sketches as the production answer.
