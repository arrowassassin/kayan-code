class Solution:
    def maxArea(self, height: list[int]) -> int:
        lo, hi = 0, len(height) - 1
        best = 0
        while lo < hi:
            if height[lo] <= height[hi]:
                best = max(best, height[lo] * (hi - lo))
                lo += 1        # shorter wall: every other pairing of lo is provably worse
            else:
                best = max(best, height[hi] * (hi - lo))
                hi -= 1
        return best
