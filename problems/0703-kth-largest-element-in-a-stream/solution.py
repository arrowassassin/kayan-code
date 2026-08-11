import heapq


class KthLargest:
    """Min-heap of the k largest values seen so far. Its root (the smallest
    of those k) IS the k-th largest. O(log k) per add, O(k) space."""

    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        while len(self.heap) > k:       # keep only the k largest
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:        # val displaces the current k-th largest
            heapq.heapreplace(self.heap, val)
        return self.heap[0]
