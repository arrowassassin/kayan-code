# Word Break — Editorial

## 1. Pattern recognition

"Can this string be segmented using pieces from a dictionary?" is **partition DP on prefixes**. The giveaways: the answer for the whole string is composed from answers for shorter pieces, there are exponentially many segmentations but only `n+1` cut positions, and a yes/no question ("can it be done") rather than "in how many ways" — which usually means a boolean table with an OR over choices. Its follow-up, Decode Ways (91), is the same scan with OR swapped for +: instead of "is any split valid" you count them.

## 2. Brute force first

Recursive peeling: try every dictionary word (or every prefix) that matches the front of `s`, recurse on the rest. Correct — and exponential. The classic killer input is `s = "aaa...ab"` with dictionary `{"a","aa","aaa",...}`: every prefix of a's matches many words, the recursion branches at every level, and the final unmatched `"b"` means *every* path is fully explored — O(2^n) paths for a 300-character string. Yet each recursive call is fully described by one number: the position where the unprocessed suffix begins. Only 301 distinct calls exist.

## 3. The key insight

**Whether the remaining suffix can be segmented depends only on the split position, not on which words produced it — so one boolean per position suffices: `dp[i]` = "prefix `s[:i]` is breakable".**

## 4. Step-by-step derivation

1. **Name the state.** `can(i)` = "the suffix starting at `i` can be segmented" (or, mirrored, `dp[i]` on prefixes). The history of words used so far is irrelevant to the future — that "memorylessness" is precisely what licenses the state.
2. **Say the choice out loud.** "Any valid segmentation of `s[:i]` ends with some last word `s[j:i]`. I don't know where that word starts, so I try every `j`: if `s[:j]` is breakable AND `s[j:i]` is a dictionary word, then `s[:i]` is breakable." An OR over choices.
3. **Base case:** `dp[0] = True` — the empty prefix needs zero words. This is what lets the first real word anchor to something.
4. **Why memoization collapses the cost:** the exponential brute force asks only `n+1` distinct questions; caching each answer once gives `O(n)` states × `O(n)` split points × `O(L)` slicing/hashing — polynomial. The `"aaa...ab"` bomb becomes a few thousand cheap lookups.
5. **Two practical constant-factor wins:** put `wordDict` in a **set** (each membership test is O(len) hashing instead of scanning 1000 words), and only look back `max_len` characters — no dictionary word is longer than 20, so `j` ranges over at most 20 positions, making the real cost O(n · max_len · max_len).

## 5. Annotated Python solution

```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)                  # O(1) membership tests
        max_len = max(map(len, words))         # words are short; don't scan further back
        n = len(s)
        dp = [False] * (n + 1)                 # dp[i] = s[:i] is breakable
        dp[0] = True                           # empty prefix: zero words needed
        for i in range(1, n + 1):
            for j in range(max(0, i - max_len), i):
                if dp[j] and s[j:i] in words:  # breakable prefix + one final word
                    dp[i] = True
                    break                      # one witness is enough (it's an OR)
        return dp[n]
```

## 6. Complexity

- **Time O(n · L²)** with `L` = longest word length (≤ 20) — "each of n positions looks back at most L split points, and each check slices/hashes a ≤ L substring." Without the `max_len` cutoff: O(n² · n) worst case — still fine at n = 300.
- **Space O(n)** for the table plus O(total dictionary size) for the set.

## 7. Edge-case traps

- **Single character** — `("a", ["a"])` → true, `("a", ["b"])` → false; off-by-one in `dp[0]`/`dp[n]` shows up immediately here.
- **Reuse is allowed** — `"applepenapple"`; a solution that removes words from the dictionary as it uses them is wrong.
- **Overlapping candidates** — `"cars"` with `["car","ca","rs"]`: the greedy longest-match (`"car"` + stranded `"s"`) fails; DP explores `"ca" + "rs"`. Greedy matching is the classic wrong turn here.
- **The exponential bomb** — `"aaa...ab"` with an all-a dictionary: any submission without memoization TLEs on the hidden suite.
- **Whole string is one word** — the `j = 0` split with `dp[0] = True` must be reachable; that's exactly what the base case encodes.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion)** — peel words off the front, cache by position:

```python
from functools import lru_cache

class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        max_len = max(map(len, words))

        @lru_cache(maxsize=None)
        def can(i: int) -> bool:               # can s[i:] be segmented?
            if i == len(s):
                return True                    # base case: nothing left
            for k in range(i + 1, min(i + max_len, len(s)) + 1):
                if s[i:k] in words and can(k): # first word s[i:k], recurse on rest
                    return True
            return False

        return can(0)
```

**Bottom-up (iterative table)** — section 5 above (mirrored to prefixes). **The mechanical conversion recipe:**

1. **State → params → table index.** The memo key is the position `i`; it becomes the table index `dp[i]`.
2. **Memo → table.** `@lru_cache` becomes `dp = [False] * (n + 1)` — one boolean per state.
3. **Recursion order → loop order.** `can(i)` depends on *larger* indices, so the loop must run the opposite direction. Iterating suffixes right-to-left, or (equivalently, flipping the state to prefixes) left-to-right as in section 5 — either way, every value on the right-hand side is filled before it's read.
4. **Base case → initialization.** `if i == n: return True` becomes `dp[0] = True` (prefix form) written before the loop; unfilled cells start `False`, matching the "no witness found" default.

## 9. Interviewer follow-up

- **"Return the actual sentences"** — Word Break II (140): same recursion, but memoize the *list of segmentations* per position; output can be exponential, so state that up front.
- **"Count the segmentations"** — swap the OR for a sum: `dp[i] += dp[j]` whenever `s[j:i]` is a word. That is structurally Decode Ways (91), this problem's linked follow-up, where the "dictionary" is the codes 1–26.
- **"Huge dictionary, long words?"** — build a trie of the words and walk it from each position; the trie prunes dead prefixes without hashing every slice, replacing the O(L²) slicing term with O(L) per position.
