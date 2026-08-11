from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = defaultdict(list)
        for s in strs:
            counts = [0] * 26                    # letter histogram: O(L) per word
            for ch in s:
                counts[ord(ch) - 97] += 1
            groups[tuple(counts)].append(s)      # tuple -> hashable canonical key
        return list(groups.values())
