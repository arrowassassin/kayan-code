class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        n = len(nums)
        for i in range(n - 2):
            if nums[i] > 0:                      # smallest value positive -> no zero sum possible
                break
            if i > 0 and nums[i] == nums[i - 1]: # same anchor value -> same triplets; skip
                continue
            lo, hi = i + 1, n - 1
            target = -nums[i]
            while lo < hi:
                s = nums[lo] + nums[hi]
                if s < target:
                    lo += 1
                elif s > target:
                    hi -= 1
                else:
                    res.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:  # skip duplicate second values
                        lo += 1
        return res
