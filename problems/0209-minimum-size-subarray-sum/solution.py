class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        best = float("inf")
        window_sum = 0
        left = 0
        for right, x in enumerate(nums):
            window_sum += x
            # valid -> harvest at every shrink step, then tighten
            while window_sum >= target:
                best = min(best, right - left + 1)
                window_sum -= nums[left]
                left += 1
        return 0 if best == float("inf") else best
