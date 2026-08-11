import heapq


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        # Min-heap of the k largest values seen so far.
        # Its root (the smallest of the keepers) is the answer.
        heap = nums[:k]
        heapq.heapify(heap)                 # O(k)
        for x in nums[k:]:
            if x > heap[0]:                 # beats the current weakest keeper
                heapq.heapreplace(heap, x)  # pop root + push in one sift
        return heap[0]
