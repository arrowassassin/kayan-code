# Implement Trie (Prefix Tree) — Editorial

## 1. Pattern recognition

The statement pairs whole-word lookup with **prefix** lookup. The moment "prefix" appears as a first-class query, hash sets lose their magic: hashing scrambles a string's structure, so a set can say "is `apple` here?" in O(1) but can only answer "does anything start with `app`?" by checking every member. The signal to read is *queries that respect the left-to-right structure of strings* → build a structure shaped like that structure: a **trie**. This problem is the entry point of the Tries topic — every later trie problem (Word Search II, autocomplete, word dictionaries with wildcards) is this class plus one twist.

## 2. Brute force first

Store all words in a Python set. `insert` and `search` are O(1) average, but `startsWith(p)` becomes `any(w.startswith(p) for w in words)` — O(N·L) per query. With up to 3×10⁴ calls, tens of thousands of stored words, and words up to 2,000 characters, that's on the order of 10⁸–10⁹ character comparisons: it TLEs, and more tellingly it does *zero* sharing between queries — checking `app` teaches it nothing about `appl`. (Storing every prefix of every word in a second set fixes the time but costs O(total chars²) memory in the worst case — worth *saying* in an interview, then discarding.)

## 3. The key insight

**Store words as root-to-leaf paths in a tree keyed by letters, so every shared prefix is stored exactly once — and both queries become the same walk down that tree.**

## 4. Step-by-step derivation

1. If many words share a beginning, store the beginning once: a tree where each edge carries one letter. `cat` and `car` share the path `c → a`, then fork. A prefix exists **iff its path exists** — `startsWith` is now a walk, not a scan.
2. What is a node, concretely? It only needs "which letters continue from here" — a mapping letter → child. In Python the lightest honest answer is a **plain dict per node**; nested dicts *are* the trie. (A `TrieNode` class with a 26-slot array is the same idea with different constant factors — mention it, don't start there.)
3. `insert` walks the word, creating missing children as it goes — `setdefault(ch, {})` does "follow or create" in one call.
4. One problem left: after inserting only `apple`, the path for `app` exists, so a naive `search("app")` wrongly says yes. Paths prove *prefixes*, not *words*. So mark word-ends explicitly: plant a sentinel key (`"$"`, impossible as a letter) in the final node. Now `search` = walk **and** demand the marker; `startsWith` = walk alone. The two methods share every line except the last check — write the walk once.
5. Re-inserting a word just re-walks existing nodes and re-sets the marker — idempotent for free.

## 5. Annotated Python solution

```python
class Trie:
    def __init__(self):
        self.root = {}                      # node = dict: letter -> child node

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})  # follow the edge, creating it if absent
        node["$"] = True                    # sentinel: "a word ends at this node"

    def _walk(self, s):                     # shared walk: node at end of path, or None
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and "$" in node   # path alone isn't enough — need the marker

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None     # path alone IS enough
```

## 6. Complexity

- **Time O(L)** per operation, `L` = length of the argument — "one dict hop per character, independent of how many words are stored."
- **Space O(total characters inserted)** worst case — "at most one node per character, and shared prefixes share nodes, so it's often far less."

## 7. Edge-case traps

- **A word that is a prefix of another** — insert `apple` only: `search("app")` must be `False` while `startsWith("app")` is `True`. Forgetting the end marker (or checking it in `startsWith`) breaks exactly one of these — the classic trie bug, in both directions.
- **The reverse order** — insert `app` only: `search("apple")` must be `False`; the walk must fail cleanly on a missing edge, not crash or default.
- **Query longer than any path** (`startsWith("hellos")` after inserting `hello`) — the walk runs off the tree; return `False`, don't KeyError.
- **Single-character words** — the loop body runs once; the marker lands one level below the root.
- **Repeated inserts** must not duplicate nodes or flip any answer.
- **Marker key collisions** — the sentinel must be a value no input letter can be (`"$"` beats `True`-as-a-key hacks); with a node class, it's a boolean field instead.

## 8. (DP section — not applicable)

Not DP. The reusable skill is the character-walk trie template — the identical node-dict + end-marker skeleton underlies Word Search II, Design Add and Search Words, and autocomplete systems.

## 9. Interviewer follow-up

- *"Now return all words with a given prefix"* (autocomplete) — walk to the prefix node in O(L), then DFS the subtree collecting words; rank real autocomplete by storing a top-k list or hit count per node.
- *"Search with wildcards"* (`.` matches any letter — Design Add and Search Words 211) — same walk, but a `.` branches into every child: recursion with backtracking; complexity degrades toward O(26^dots).
- *"Find many words in a letter grid"* (Word Search II 212) — insert the dictionary into a trie, then DFS the grid *and* the trie in lockstep, pruning any grid path the trie doesn't extend — the trie's prefix-sharing is what makes the pruning powerful.
- *"Memory is tight"* — 26-slot arrays vs dicts trade-offs, then compressed tries (radix trees) that collapse single-child chains, and DAWGs that also merge common suffixes.
