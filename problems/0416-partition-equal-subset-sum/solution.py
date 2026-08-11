class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:                        # odd total: no equal split
            return False
        target = total // 2
        # dp[s] = some subset of the numbers seen so far sums to s
        dp = [False] * (target + 1)
        dp[0] = True                         # empty subset
        for x in nums:
            # iterate s downward so each number is used at most once
            for s in range(target, x - 1, -1):
                if dp[s - x]:
                    dp[s] = True
            if dp[target]:                   # early exit
                return True
        return dp[target]
