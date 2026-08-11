class Solution:
    def longestPalindrome(self, s: str) -> str:
        best_lo, best_hi = 0, 1                  # best window [lo, hi)

        def expand(lo: int, hi: int) -> None:
            # grow symmetrically while the mirror characters agree
            nonlocal best_lo, best_hi
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1
                hi += 1
            if (hi - 1) - (lo + 1) + 1 > best_hi - best_lo:
                best_lo, best_hi = lo + 1, hi    # last valid window

        for c in range(len(s)):
            expand(c, c)                         # odd length: center at c
            expand(c, c + 1)                     # even length: center between c, c+1
        return s[best_lo:best_hi]
