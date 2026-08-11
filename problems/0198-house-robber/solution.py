class Solution:
    def rob(self, nums: list[int]) -> int:
        # take = best total if we rob the current house
        # skip = best total if we don't
        take, skip = 0, 0
        for x in nums:
            # rob this house -> we must have skipped the previous one
            # skip this house -> carry the better of the two previous states
            take, skip = skip + x, max(take, skip)
        return max(take, skip)
