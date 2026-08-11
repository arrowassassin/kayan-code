from collections import defaultdict


class Solution:
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
        def at_most(k: int) -> int:
            count = defaultdict(int)
            left = total = 0
            for right, x in enumerate(nums):
                count[x] += 1
                while len(count) > k:
                    count[nums[left]] -= 1
                    if count[nums[left]] == 0:
                        del count[nums[left]]
                    left += 1
                # every subarray ending at `right` starting in [left, right]
                total += right - left + 1
            return total

        # exactly k = (at most k) - (at most k-1)
        return at_most(k) - at_most(k - 1)
