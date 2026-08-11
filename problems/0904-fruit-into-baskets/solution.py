from collections import defaultdict


class Solution:
    def totalFruit(self, fruits: list[int]) -> int:
        count = defaultdict(int)   # type -> occurrences inside the window
        best = left = 0
        for right, f in enumerate(fruits):
            count[f] += 1
            # invariant: at most 2 distinct types in the window
            while len(count) > 2:
                count[fruits[left]] -= 1
                if count[fruits[left]] == 0:
                    del count[fruits[left]]   # delete so len() stays truthful
                left += 1
            best = max(best, right - left + 1)
        return best
