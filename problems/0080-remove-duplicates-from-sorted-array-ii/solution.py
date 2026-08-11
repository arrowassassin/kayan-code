class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        write = 0
        for x in nums:
            # keep x unless the last two kept values are both already x
            if write < 2 or nums[write - 2] != x:
                nums[write] = x
                write += 1
        return write
