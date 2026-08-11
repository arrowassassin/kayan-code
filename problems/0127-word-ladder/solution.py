from collections import deque
from string import ascii_lowercase


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        words = set(wordList)               # O(1) membership
        if endWord not in words:
            return 0

        queue = deque([(beginWord, 1)])     # (word, chain length so far)
        words.discard(beginWord)            # never revisit the start
        while queue:
            word, length = queue.popleft()
            if word == endWord:
                return length
            for i in range(len(word)):
                for ch in ascii_lowercase:
                    nxt = word[:i] + ch + word[i + 1:]
                    if nxt in words:
                        words.remove(nxt)   # mark visited on enqueue
                        queue.append((nxt, length + 1))
        return 0
