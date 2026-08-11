from collections import Counter


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = Counter()
        max_freq = 0        # best single-letter frequency EVER seen in a window
        left = 0
        for right, c in enumerate(s):
            count[c] += 1
            max_freq = max(max_freq, count[c])
            # window invalid -> slide (never shrink below best size found)
            if (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
        # window length ends at the largest valid size reached
        return len(s) - left
