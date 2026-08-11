class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        # prev[j] = edit distance between word1[:i-1] and word2[:j]
        prev = list(range(n + 1))              # row 0: build word2[:j] by j inserts
        for i in range(1, m + 1):
            cur = [i] + [0] * n                # column 0: delete all i chars
            c1 = word1[i - 1]
            for j in range(1, n + 1):
                if c1 == word2[j - 1]:
                    cur[j] = prev[j - 1]       # free: last chars already agree
                else:
                    cur[j] = 1 + min(
                        prev[j - 1],           # replace word1's last char
                        prev[j],               # delete  word1's last char
                        cur[j - 1],            # insert  word2's last char
                    )
            prev = cur
        return prev[n]
