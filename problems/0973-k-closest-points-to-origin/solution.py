import heapq


class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        # We want the k SMALLEST distances, so the bounded heap must evict
        # its current WORST (largest) — i.e. we need a max-heap of size k.
        # heapq is a min-heap, so store negated squared distances.
        # sqrt is monotonic -> comparing squared distances is exact and int-only.
        heap = []                                   # (-dist2, x, y)
        for x, y in points:
            d2 = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-d2, x, y))
            elif -d2 > heap[0][0]:                  # closer than current worst
                heapq.heapreplace(heap, (-d2, x, y))
        return [[x, y] for _, x, y in heap]
