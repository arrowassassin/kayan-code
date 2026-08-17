class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        def days_needed(cap: int) -> int:
            # greedy: fill each day until the next package would overflow
            d, load = 1, 0
            for w in weights:
                if load + w > cap:
                    d += 1
                    load = 0
                load += w
            return d

        lo, hi = max(weights), sum(weights)
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid            # mid suffices -> answer is mid or smaller
            else:
                lo = mid + 1        # too small -> answer strictly larger
        return lo
