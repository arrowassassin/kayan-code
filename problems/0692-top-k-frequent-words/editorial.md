# Top K Frequent Words — Editorial

## 1. Pattern recognition

Same skeleton as Top K Frequent Elements (this problem's warmup): "most frequent" → hash-map counting pass, "top k" → top-k ranking. The new signal is the **deterministic output order with a two-field tie-break** — frequency descending, word ascending. When the two criteria point in *opposite directions*, the problem is really testing whether you can encode a composite ranking rule as a single comparison key. That skill, not the heap, is what this problem adds.

## 2. Brute force first

Count, then sort the distinct words with a custom comparator and slice k: O(d log d) for d distinct words. With d ≤ 5·10⁴ this passes easily, and honestly it's a fine interview answer *if you get the key right*. The upgrade to O(d log k) with a bounded heap matters when d is huge and k tiny (autocomplete over millions of words, k=10) — and the interviewer will probe whether you can make a heap respect the tie-break, which is where candidates who "just negate everything" get stuck.

## 3. The key insight

**Encode "frequency descending, word ascending" as the single tuple key `(-count, word)` — numbers can be negated to flip their direction, so the composite rule collapses into ordinary "smallest key wins".**

## 4. Step-by-step derivation

1. Count: `counts = Counter(words)`, O(n) — identical to the warmup.
2. Write the ranking rule as a key. Python compares tuples lexicographically, so `(-count, word)` orders by count descending first, word ascending second. The asymmetry is important: you can negate a count, but there is no clean "negate" for a string — so always flip the *numeric* field and leave the string field in its natural direction. (If you ever must flip a string's direction inside a min-heap, that needs a wrapper class with a reversed `__lt__` — worth mentioning, painful to write.)
3. Sort answer: `sorted(counts, key=...)[:k]` — O(d log d), done.
4. Heap answer: `heapq.nsmallest(k, counts, key=...)` keeps a heap bounded at size k while scanning the d candidates → O(d log k). Note it's `nsmallest`, not `nlargest`: negating the count already made the best key the *smallest*. Under the hood, Python's `heapq` is a min-heap either way; `nsmallest` internally maintains a max-heap-of-k via key inversion, so you get the bounded-heap behavior without hand-rolling it.
5. What about the warmup's O(n) bucket sort? It still applies — bucket words by count — but each bucket must be sorted alphabetically before emission. That costs O(d log d) in the worst case (all words in one bucket), so **the deterministic tie-break erases the bucket sort's linear-time advantage**. Recognizing that "any order" was load-bearing in 347 is exactly the k-vs-n maturity interviewers look for.

## 5. Annotated Python solution

```python
import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        counts = Counter(words)                 # O(n) counting pass
        # (-count, word): count DESC via negation, word ASC naturally.
        # Best candidate == smallest key, so nsmallest — which runs a
        # size-k heap over the d distinct words — emits the answer
        # already in the required order.
        return heapq.nsmallest(k, counts, key=lambda w: (-counts[w], w))
```

The explicit-sort equivalent (same key, simpler to defend under pressure):

```python
from collections import Counter


class Solution:
    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        counts = Counter(words)
        return sorted(counts, key=lambda w: (-counts[w], w))[:k]
```

## 6. Complexity

- Heap: **Time O(n + d log k)**, **Space O(d)** — "one counting pass, then each distinct word does at most one log-k heap operation."
- Sort: **Time O(n + d log d)**, **Space O(d)** — "count, then one comparison sort over the distinct words only."

## 7. Edge-case traps

- **Ties everywhere** (`["b","a"]`, k=2 → `["a","b"]`) — output must be alphabetical within equal counts; a heap keyed on count alone returns arbitrary tie order.
- **Prefix words** (`["a","aa","aaa"]`) — string comparison handles prefixes correctly (`"a" < "aa"`), but hand-rolled comparators often don't.
- **k equal to the number of distinct words** — the answer is *all* words, still in the specified order.
- **Every word identical** — one candidate, k=1; degenerate but must not crash the heap path.
- Negating the word instead of the count (or sorting `(count, word)` ascending and slicing the wrong end) — both produce plausible-looking wrong answers that only tie-heavy tests catch.

## 8. Reusable template

Not DP. This trains the **composite-key top-k** template: encode a multi-criteria ranking as a single tuple with negated numeric fields — the same move that powers K Closest Points, scheduling by (priority, timestamp), and any "order by X desc, Y asc" requirement.

## 9. Interviewer follow-up

- *"Stream of words, query top-k at any moment"* — keep a running count map; per query run size-k selection over distinct words, or maintain a count-bucket structure with doubly linked frequency buckets for O(1) updates (the LFU-cache machinery).
- *"Doesn't fit in memory (log files across machines)"* — per-shard counts, merge by sum, then top-k on the merged map; mention count-min sketch + heap for approximate top-k at scale.
- *"Why not bucket sort like the integer version?"* — you can, but sorting inside buckets restores the log factor; be ready to articulate that the tie-break rule is what changed the complexity landscape.
- *"k-th most frequent word only?"* — same key, quickselect over the (key, word) pairs: average O(d).
