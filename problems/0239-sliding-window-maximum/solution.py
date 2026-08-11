from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq = deque()   # indices; values strictly decreasing front -> back
        out = []
        for i, x in enumerate(nums):
            # x dominates every smaller-or-equal value behind it
            while dq and nums[dq[-1]] <= x:
                dq.pop()
            dq.append(i)
            # front has slid out of the window
            if dq[0] <= i - k:
                dq.popleft()
            if i >= k - 1:
                out.append(nums[dq[0]])
        return out
