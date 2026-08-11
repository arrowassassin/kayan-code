from collections import deque


class MovingAverage:
    """Bounded deque + running sum: evict the oldest value the moment the
    window overflows, keeping the sum in sync. O(1) per next, O(size) space."""

    def __init__(self, size: int):
        self.size = size
        self.window = deque()
        self.total = 0

    def next(self, val: int) -> float:
        self.window.append(val)
        self.total += val
        if len(self.window) > self.size:
            self.total -= self.window.popleft()
        return self.total / len(self.window)
