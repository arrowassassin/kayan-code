# K Closest Points to Origin — Editorial

## 1. Pattern recognition

"K closest" is the Top-K pattern wearing geometry clothes: rank n items by a derived key (distance) and keep the best k, answer in any order. Two statement details point at the intended refinements: Euclidean distance invites the **monotonic-key simplification** (skip the square root), and "any order" plus large n invites something cheaper than a full sort. The twist relative to Kth Largest: here you want the k *smallest* keys, which flips the heap orientation — the half of the pattern people fumble.

## 2. Brute force first

Compute every distance, sort the points by it, slice the first k: O(n log n). At n = 10⁵ it passes — sorting is not the villain here. But this problem is chosen precisely to test whether you can run the top-k template in the *minimum* direction, and whether you notice that computing `sqrt` at all is unnecessary work (and a float-precision liability). Open with "sort works in n log n; a bounded heap gives n log k; quickselect averages O(n)" and let the interviewer pick the depth.

## 3. The key insight

**To keep the k smallest distances you must be able to evict the current worst — so the bounded heap must be a max-heap, which in Python's min-heap-only `heapq` means storing negated (squared) distances.**

## 4. Step-by-step derivation

1. Simplify the key: `sqrt` is monotonic, so comparing `x² + y²` gives identical rankings using exact integer arithmetic. Say this before writing code — it's a free correctness *and* performance point.
2. Maintain a pool of the k best (smallest-key) points seen so far. A new point enters only if it beats the pool's **worst** member, so the pool must expose its *maximum* — a max-heap. (Contrast with Kth Largest, where keeping the k largest needed the pool's minimum → min-heap. The rule: the heap's root is always the eviction candidate.)
3. Python's `heapq` only does min-heaps, so negate: push `(-d2, x, y)`; the root then holds the largest true distance. Tuple comparison never reaches the coordinates unless distances tie, and ties compare ints — safe.
4. Push the first k points; after that, compare each new point against `heap[0]` and `heapreplace` when it's closer. Each of n points costs at most one O(log k) operation → **O(n log k)**, **O(k)** space, and the loop works unchanged on a stream.
5. If asked for better: quickselect on squared distance partitions the array around a random pivot and recurses into the side containing index k — average **O(n)**, worst O(n²), in-place, needs the whole array. The heap-vs-quickselect trade-off is the same conversation as Kth Largest; here `heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)` is the one-line library form of the heap answer.

## 5. Annotated Python solution

```python
import heapq


class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        # Bounded MAX-heap of the k closest points; heapq is min-only,
        # so store -dist². Squared distance: sqrt is monotonic, ints exact.
        heap = []                                   # (-dist2, x, y)
        for x, y in points:
            d2 = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-d2, x, y))
            elif -d2 > heap[0][0]:                  # strictly closer than the worst keeper
                heapq.heapreplace(heap, (-d2, x, y))  # evict + insert, one sift
        return [[x, y] for _, x, y in heap]         # any order is fine
```

## 6. Complexity

- **Time O(n log k)** — "every point does at most one push or replace into a heap that never grows past k."
- **Space O(k)** — "only the k current keepers live in memory, which is why this version survives a stream."

## 7. Edge-case traps

- **k = n** — every point is returned; the `len(heap) < k` branch absorbs the whole input and the eviction branch never runs.
- **The origin itself in the input** (`[0,0]`, d² = 0) — must be handled naturally, and negation of 0 must not confuse anyone hand-rolling comparisons.
- **Negative coordinates** — squaring makes them positive; the bug appears when someone compares `x + y` or forgets parentheses in a manual distance.
- **Wrong heap orientation** — using a min-heap of positive distances with the same size-k eviction silently keeps the k *farthest* points; small tests with k = 1 catch it instantly.
- **Float `sqrt` comparisons** — with coordinates up to 10⁴, squared distances reach 2·10⁸: exact in ints, but two nearly-equal `sqrt` values can misorder under float rounding. Integer squared distance sidesteps the whole class of bug.

## 8. Reusable template

Not DP. This trains the **bounded max-heap for bottom-k** template — the mirror image of Kth Largest's min-heap — plus the negation idiom that Python's min-only `heapq` forces on every "keep the smallest" problem.

## 9. Interviewer follow-up

- *"Points arrive as an infinite stream"* — the heap loop already works: O(k) memory, one heap op per arrival; quickselect and sorting are disqualified.
- *"Average O(n)?"* — quickselect on squared distance with random pivots; discuss the O(n²) worst case and why random pivots make it acceptable.
- *"K closest to an arbitrary query point, many queries"* — precompute nothing per-query; build a k-d tree or grid index instead — recognize when the repeated-query regime changes the right structure.
- *"Manhattan distance instead?"* — only the key function changes; the template is untouched. That separation (key extraction vs. selection machinery) is the sign of a clean solution.
