class Solution:
    def numDecodings(self, s: str) -> int:
        # two_back = ways to decode s[:i-1], one_back = ways to decode s[:i]
        two_back, one_back = 1, 1 if s[0] != "0" else 0
        for i in range(1, len(s)):
            cur = 0
            if s[i] != "0":                       # single digit 1-9
                cur += one_back
            if "10" <= s[i - 1 : i + 1] <= "26":  # valid two-digit code
                cur += two_back
            two_back, one_back = one_back, cur
        return one_back
