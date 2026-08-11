class Solution:
    def sortColors(self, nums: list[int]) -> None:
        lo, mid, hi = 0, 0, len(nums) - 1
        # invariant: nums[:lo] == 0s, nums[lo:mid] == 1s, nums[hi+1:] == 2s
        while mid <= hi:
            if nums[mid] == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1
                mid += 1          # swapped-in value came from the known-1 zone
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1           # do NOT advance mid: the swapped-in value is unexamined
