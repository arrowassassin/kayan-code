from collections import deque


class HitCounter:
    """Deque of (timestamp, count) pairs, compressed so equal timestamps
    share one entry. A running total makes getHits O(1) after eviction;
    eviction is amortized O(1) — each entry is popped at most once."""

    def __init__(self):
        self.events = deque()   # (timestamp, hits at that timestamp)
        self.total = 0

    def _evict(self, timestamp: int) -> None:
        while self.events and self.events[0][0] <= timestamp - 300:
            _, cnt = self.events.popleft()
            self.total -= cnt

    def hit(self, timestamp: int) -> None:
        if self.events and self.events[-1][0] == timestamp:
            ts, cnt = self.events[-1]
            self.events[-1] = (ts, cnt + 1)
        else:
            self.events.append((timestamp, 1))
        self.total += 1
        self._evict(timestamp)

    def getHits(self, timestamp: int) -> int:
        self._evict(timestamp)
        return self.total
