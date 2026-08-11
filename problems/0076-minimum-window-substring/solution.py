from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(t) > len(s):
            return ""

        need = Counter(t)          # how many of each char the window still lacks
        missing = len(t)           # total characters still lacking (with multiplicity)
        best_len = float("inf")
        best_left = 0
        left = 0

        for right, c in enumerate(s):
            if need[c] > 0:        # this char was still needed
                missing -= 1
            need[c] -= 1           # may go negative: surplus copies

            while missing == 0:    # window covers t -> harvest, then shrink
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_left = left
                lc = s[left]
                need[lc] += 1
                if need[lc] > 0:   # we just dropped a required copy
                    missing += 1
                left += 1

        return "" if best_len == float("inf") else s[best_left:best_left + best_len]
