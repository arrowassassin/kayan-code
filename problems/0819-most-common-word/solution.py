class Solution:
    def mostCommonWord(self, paragraph: str, banned: list[str]) -> str:
        banned_set = set(banned)
        counts = {}
        best, best_count = "", 0
        word = []
        # sentinel "." guarantees the last word gets flushed
        for ch in paragraph + ".":
            if ch.isalpha():
                word.append(ch.lower())          # normalize case as we read
            elif word:
                w = "".join(word)
                word = []
                if w not in banned_set:
                    c = counts.get(w, 0) + 1
                    counts[w] = c
                    if c > best_count:
                        best, best_count = w, c
        return best
