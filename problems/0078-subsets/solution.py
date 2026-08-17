class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        path = []

        def backtrack(start: int) -> None:
            # every node of the decision tree is a valid subset
            res.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])      # choose
                backtrack(i + 1)          # explore
                path.pop()                # unchoose

        backtrack(0)
        return res
