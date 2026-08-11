import heapq


class MedianFinder:
    """Two heaps split the stream around the median:
    lo = max-heap of the smaller half (negated: heapq is min-only),
    hi = min-heap of the larger half.
    Invariants: every lo value <= every hi value; len(lo) - len(hi) in {0, 1}.
    """

    def __init__(self):
        self.lo = []   # max-heap via negation; holds the extra element when n is odd
        self.hi = []   # min-heap

    def addNum(self, num: int) -> None:
        # Route through lo first, then rebalance the sizes.
        heapq.heappush(self.lo, -num)
        # Ordering invariant: lo's max must not exceed hi's min.
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Size invariant: lo owns the odd element.
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0
