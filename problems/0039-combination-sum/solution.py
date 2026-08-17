class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()                 # enables clean pruning
        res = []
        path = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break                 # sorted: everything after is too big too
                path.append(candidates[i])        # choose
                backtrack(i, remaining - candidates[i])  # i, not i+1: reuse allowed
                path.pop()                        # unchoose

        backtrack(0, target)
        return res
