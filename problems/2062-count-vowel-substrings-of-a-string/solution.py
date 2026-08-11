class Solution:
    def countVowelSubstrings(self, word: str) -> int:
        VOWELS = frozenset("aeiou")
        total = 0
        run_start = 0        # left edge of the current all-vowel run
        last = {}            # vowel -> most recent index inside the run
        for i, ch in enumerate(word):
            if ch not in VOWELS:
                # consonant: every substring crossing i is disqualified
                run_start = i + 1
                last.clear()
                continue
            last[ch] = i
            if len(last) == 5:
                # any start in [run_start, min(last seen)] works with end = i
                total += min(last.values()) - run_start + 1
        return total
