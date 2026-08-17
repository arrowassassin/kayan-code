class Solution:
    def splitArray(self, nums: list[int], k: int) -> int:
        def pieces_needed(limit: int) -> int:
            # greedy: extend the current block until adding would exceed limit
            pieces, total = 1, 0
            for x in nums:
                if total + x > limit:
                    pieces += 1
                    total = 0
                total += x
            return pieces

        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if pieces_needed(mid) <= k:
                hi = mid            # limit achievable -> try smaller
            else:
                lo = mid + 1        # too many pieces forced -> raise limit
        return lo
