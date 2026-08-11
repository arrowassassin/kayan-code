## Hint 1

Forget "words" for a moment. If every word is a node and two words are joined when they differ in one letter, what kind of question is "shortest transformation sequence"? Which traversal answers shortest-path questions on unweighted graphs?

## Hint 2

Building the graph by comparing all pairs of words costs O(N² · L) — 5000² comparisons is too slow. Instead, generate a word's neighbors directly: for each of its `L` positions, substitute each of the 26 letters and check membership in a **set** built from `wordList`. That's `26·L` probes per word.

## Hint 3

BFS from `beginWord`, storing `(word, chain_length)` in a deque with the start at length 1. When you generate a neighbor that's in the word set, **remove it from the set immediately** (visited-on-enqueue) — removal doubles as the visited set and shrinks future probes. Return the length when you pop `endWord`; return 0 if the queue drains. Check `endWord in wordList` up front for a fast exit.
