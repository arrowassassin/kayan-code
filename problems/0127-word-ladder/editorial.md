# Word Ladder — Editorial

## 1. Pattern recognition

Strip the story: words are nodes, "differs in exactly one letter" is an edge, and the question is the **length of the shortest path** from one node to another. Unweighted shortest path means **BFS**, full stop — DFS finds *a* chain, not the shortest one. What makes this Hard isn't the traversal; it's noticing that the graph is *implicit* and that materializing it naively is the real cost. The interview skill on display: converting a string puzzle into a graph, then choosing how to enumerate edges without building them all.

## 2. Brute force first

Two layers of brute force to reject aloud. First, DFS/backtracking over all chains — exponential, and it can wander down a length-4990 chain before trying the short one. Second, BFS but with the graph built by pairwise comparison: N² word pairs at L characters each is O(N²·L) = 5000² × 10 = 2.5 × 10⁸ character comparisons just for edges — the 3-second stress test with 4990 words is designed to kill exactly this. The insight to fish for: a node's neighbors can be *generated* faster than they can be *searched for*.

## 3. The key insight

**Neighbors of a word are enumerable directly — try all 26 letters in each of its L positions and test membership in a hash set — so BFS runs on the implicit graph at 26·L probes per node with no edge list ever built.**

## 4. Step-by-step derivation

1. Load `wordList` into a set: O(1) membership. If `endWord` isn't in it, return 0 immediately — no chain may end outside the dictionary.
2. BFS from `beginWord` with chain length 1 (lengths count words, not steps — a classic off-by-one to state explicitly).
3. To expand a word: for each position `i`, for each letter `c`, form `word[:i] + c + word[i+1:]` and check the set. 26 × 10 = 260 probes per node beats scanning 5000 candidates per node by orders of magnitude.
4. Visited-set discipline, the sharpest version of it in this topic: **remove a word from the set the moment you enqueue it**. Removing on *dequeue* instead lets an entire BFS layer enqueue the same popular word — on dense dictionaries that's an exponential queue blowup, the bug that turns AC into TLE with identical-looking code.
5. Deleting from the live set is safe precisely because BFS visits nodes in non-decreasing distance: the first time a word is reachable is via a shortest path, so no later path needs it.
6. Return the length carried by `endWord` when popped; a drained queue means unreachable → 0.

## 5. Annotated Python solution

```python
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
```

## 6. Complexity

- **Time O(N · 26 · L · L)** — "each of the N words is expanded once, trying 26·L substitutions, each substitution building an L-character string."
- **Space O(N · L)** — "the word set and the queue each hold at most every word once."

## 7. Edge-case traps

- **`endWord` missing from the dictionary** → 0, even if a chain of transformations could spell it.
- **Counting steps instead of words** → off by one everywhere; anchor on the example (`hit -> ... -> cog` = 5).
- **`beginWord` present in `wordList`** → must not be revisited; discard it from the set up front.
- **Visited on dequeue instead of enqueue** → correct answers on small tests, TLE on the hidden stress test; this is the trap the problem exists to teach.
- **No chain despite shared letters** (`talk -> tail` with no bridge) → the queue must drain cleanly to 0, not loop.

## 8. Reusable template

Not DP. This trains the **implicit-graph BFS template** — states generated on the fly from a rule plus a hash-set visited structure; the same skeleton solves Open the Lock, Minimum Genetic Mutation, and sliding-puzzle problems.

## 9. Interviewer follow-up

- *"Return every shortest chain, not just the length"* — Word Ladder II (126): BFS layer by layer recording parents, then backtrack from `endWord`; keep per-layer deletion so paths within one layer survive.
- *"Speed it up further"* — bidirectional BFS: expand the smaller frontier from each end; meeting in the middle cuts the explored ball from b^d to ~2·b^(d/2). Walk through why frontiers must alternate and how termination works — this is the expected Hard-level flourish.
- *"Words of length 20+, huge dictionary"* — precompute wildcard buckets (`h*t -> [hot, hat, ...]`) once in O(N·L) so expansion touches only real neighbors instead of 26 candidates per position.
