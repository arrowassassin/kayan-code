class Solution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0
        lo, hi = 0, len(height) - 1
        max_left, max_right = height[lo], height[hi]
        water = 0
        while lo < hi:
            if max_left <= max_right:
                lo += 1                      # left wall is the binding one
                max_left = max(max_left, height[lo])
                water += max_left - height[lo]
            else:
                hi -= 1
                max_right = max(max_right, height[hi])
                water += max_right - height[hi]
        return water
