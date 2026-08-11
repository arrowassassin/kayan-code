import heapq
from collections import Counter


class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        # Feasibility: the majority letter needs the other letters as spacers.
        if max(counts.values()) > (len(s) + 1) // 2:
            return ""

        # Greedy: always place the letter with the most copies LEFT,
        # except the one just used (held back for one round).
        # Max-heap via negated counts — heapq is min-only.
        heap = [(-c, ch) for ch, c in counts.items()]
        heapq.heapify(heap)

        out = []
        prev = None                          # (neg_count, ch) benched last round
        while heap:
            negc, ch = heapq.heappop(heap)   # most remaining, and != out[-1]
            out.append(ch)
            if prev:                         # benched letter is eligible again
                heapq.heappush(heap, prev)
            prev = (negc + 1, ch) if negc + 1 else None
        return "".join(out)
