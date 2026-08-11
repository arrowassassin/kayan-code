class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}          # char -> index of its most recent occurrence
        best = left = 0
        for right, c in enumerate(s):
            # duplicate inside the current window -> jump left past it
            if c in last and last[c] >= left:
                left = last[c] + 1
            last[c] = right
            best = max(best, right - left + 1)
        return best
