class Solution:
    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        lines = []
        i, n = 0, len(words)
        while i < n:
            # greedily take words while they fit with 1 space between each
            j, length = i, 0
            while j < n and length + len(words[j]) + (j - i) <= maxWidth:
                length += len(words[j])
                j += 1
            count = j - i
            if j == n or count == 1:
                # last line, or a single word: left-justify, pad right
                line = " ".join(words[i:j])
                line += " " * (maxWidth - len(line))
            else:
                spaces = maxWidth - length
                q, r = divmod(spaces, count - 1)     # left gaps get the extra space
                parts = []
                for k in range(i, j - 1):
                    parts.append(words[k])
                    parts.append(" " * (q + (1 if k - i < r else 0)))
                parts.append(words[j - 1])
                line = "".join(parts)
            lines.append(line)
            i = j
        return lines
