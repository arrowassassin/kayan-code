import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        counts = Counter(words)
        # Rank key: frequency DESC, then word ASC. Negating the count
        # turns "best" into "smallest key", so nsmallest picks the winners
        # with a size-k heap under the hood (O(d log k)).
        return heapq.nsmallest(k, counts, key=lambda w: (-counts[w], w))
