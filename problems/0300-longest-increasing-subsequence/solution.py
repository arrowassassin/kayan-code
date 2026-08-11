import bisect


class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        # tails[k] = smallest possible tail value of an increasing
        # subsequence of length k+1. tails is always sorted.
        tails = []
        for x in nums:
            i = bisect.bisect_left(tails, x)   # first tail >= x
            if i == len(tails):
                tails.append(x)                # x extends the longest run
            else:
                tails[i] = x                   # x is a better (smaller) tail
        return len(tails)
