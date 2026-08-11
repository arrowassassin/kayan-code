class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        if n > m:                              # keep the rolling row short
            text1, text2, m, n = text2, text1, n, m
        prev = [0] * (n + 1)                   # dp row for i-1 characters of text1
        for i in range(1, m + 1):
            cur = [0] * (n + 1)
            c1 = text1[i - 1]
            for j in range(1, n + 1):
                if c1 == text2[j - 1]:
                    cur[j] = prev[j - 1] + 1   # match: extend the diagonal
                else:
                    cur[j] = max(prev[j], cur[j - 1])  # drop one char from either string
            prev = cur
        return prev[n]
