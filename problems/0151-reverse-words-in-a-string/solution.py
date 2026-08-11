class Solution:
    def reverseWords(self, s: str) -> str:
        words = []
        i = len(s) - 1
        while i >= 0:
            # skip any run of spaces
            while i >= 0 and s[i] == " ":
                i -= 1
            if i < 0:
                break
            # scan the word we just landed on
            j = i
            while j >= 0 and s[j] != " ":
                j -= 1
            words.append(s[j + 1:i + 1])
            i = j
        return " ".join(words)
