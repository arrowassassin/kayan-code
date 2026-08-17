class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def hours_at(k: int) -> int:
            # ceil(p / k) per pile, summed
            return sum((p + k - 1) // k for p in piles)

        lo, hi = 1, max(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            if hours_at(mid) <= h:
                hi = mid            # mid works -> answer is mid or smaller
            else:
                lo = mid + 1        # mid too slow -> answer is strictly larger
        return lo
