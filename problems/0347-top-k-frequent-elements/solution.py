from collections import Counter


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        # Bucket sort on frequency: a count can never exceed len(nums),
        # so frequencies live in a bounded range -> no comparisons needed.
        counts = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]   # index = frequency
        for val, freq in counts.items():
            buckets[freq].append(val)

        res = []
        for freq in range(len(buckets) - 1, 0, -1):    # highest freq first
            for val in buckets[freq]:
                res.append(val)
                if len(res) == k:
                    return res
        return res
