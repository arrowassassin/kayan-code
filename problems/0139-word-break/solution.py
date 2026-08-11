class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)                       # O(1) membership
        max_len = max(map(len, words))              # no word is longer than this
        n = len(s)
        dp = [False] * (n + 1)                      # dp[i] = s[:i] is breakable
        dp[0] = True                                # empty prefix: trivially breakable
        for i in range(1, n + 1):
            # last word of the split is s[j:i] for some breakable prefix s[:j]
            for j in range(max(0, i - max_len), i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]
