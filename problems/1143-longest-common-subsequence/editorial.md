# Longest Common Subsequence — Editorial

## 1. Pattern recognition

Two sequences, an optimum over ways of aligning them — this is **two-string DP**, the workhorse behind diff tools, DNA alignment, and Edit Distance. The signature: a state of *one index per string*, i.e. a pair of prefixes, giving an `(m+1) × (n+1)` table. If you did Unique Paths (62, this problem's warmup), the picture transfers exactly: the table is a grid, computing a cell uses its up / left / diagonal neighbors, and filling order is a top-left-to-bottom-right sweep. What was "count the paths" there becomes "maximize over alignments" here — same skeleton, new payload.

## 2. Brute force first

Enumerate all 2^m subsequences of `text1` and for each check (in O(n)) whether it's a subsequence of `text2` — O(2^m · n), i.e. ~10^300 at m = 1000. The recursive form — compare last characters, branch on which string to shrink — is still exponential, but its state is just the pair of prefix lengths `(i, j)`. Only `(m+1)(n+1) ≈ 10^6` distinct calls exist; the exponential cost is recomputation, nothing else.

## 3. The key insight

**Compare the last characters of the two prefixes: if they match, they end the LCS and both prefixes shrink; if not, the LCS ignores the last character of at least one string — so `dp[i][j] = dp[i-1][j-1] + 1` on match, else `max(dp[i-1][j], dp[i][j-1])`.**

## 4. Step-by-step derivation

1. **Name the state.** `lcs(i, j)` = LCS length of `text1[:i]` and `text2[:j]`. How the earlier characters were aligned doesn't matter to the remaining suffixes — the pair of boundaries is a complete summary.
2. **Say the choice out loud, case by case.**
   - *Last characters equal* (`text1[i-1] == text2[j-1]`): "matching them costs nothing and can't hurt — any optimal alignment that skips this free match can be rewritten to take it. So take it: `1 + lcs(i-1, j-1)`." (That exchange argument is worth saying in the interview; it's why we don't also need to try the skip branches on a match.)
   - *Last characters differ*: "they can't both end the LCS, so at least one is dead weight. Try discarding each: `max(lcs(i-1, j), lcs(i, j-1))`."
3. **Base cases:** an empty prefix has LCS 0 with anything — `lcs(0, ·) = lcs(·, 0) = 0`.
4. **Why memoization collapses the cost:** the two-way branch on mismatch makes the raw tree 2^(m+n); caching by `(i, j)` caps total work at one O(1) computation per table cell → O(m·n). Exponential → quadratic purely by never re-answering a `(i, j)` pair.
5. **2-row space optimization:** row `i` reads only row `i-1` (up, diagonal) and its own left neighbor. Keep `prev` and `cur` arrays of length `n+1` — O(min(m, n)) space after swapping the strings so the shorter one indexes the columns. (A single row works too if you stash the diagonal in a temp before overwriting.)

## 5. Annotated Python solution

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        if n > m:                               # roll over the shorter string
            text1, text2, m, n = text2, text1, n, m
        prev = [0] * (n + 1)                    # dp row for text1[:i-1]
        for i in range(1, m + 1):
            cur = [0] * (n + 1)                 # cur[0] = 0: empty text2 prefix
            c1 = text1[i - 1]
            for j in range(1, n + 1):
                if c1 == text2[j - 1]:
                    cur[j] = prev[j - 1] + 1    # match: extend the diagonal
                else:
                    cur[j] = max(prev[j], cur[j - 1])   # drop from one string
            prev = cur
        return prev[n]
```

## 6. Complexity

- **Time O(m · n)** — "one constant-time cell per pair of prefixes; at 1000 × 1000 that's a million cells."
- **Space O(min(m, n))** — "each row depends only on the previous row, so two rolling rows over the shorter string suffice."

## 7. Edge-case traps

- **No common characters** → 0; make sure the mismatch branch, not an uninitialized cell, produces it.
- **Off-by-one between string index and table index** — `dp[i][j]` covers `text1[:i]`, so the characters compared are `text1[i-1]` / `text2[j-1]`. Mixing these up is *the* implementation bug here.
- **Repeated characters** (`"abcba"` vs `"abcbcba"`) — greedy "match the first occurrence" reasoning fails; only the DP explores which copy to align.
- **Subsequence ≠ substring** — `"abc"` vs `"acb"` has LCS 2, not 1; if an interviewer says "common substring," the recurrence changes (mismatch resets to 0).
- **Identical strings** → full length; a nice self-check for your indexing.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion):**

```python
from functools import lru_cache

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        @lru_cache(maxsize=None)
        def lcs(i: int, j: int) -> int:         # LCS of text1[:i], text2[:j]
            if i == 0 or j == 0:                # base case: empty prefix
                return 0
            if text1[i - 1] == text2[j - 1]:
                return lcs(i - 1, j - 1) + 1    # free match: always take it
            return max(lcs(i - 1, j), lcs(i, j - 1))
        return lcs(len(text1), len(text2))
```

(At 1000 × 1000, recursion depth can hit ~2000 — over CPython's default limit — and per-call overhead is real. Honest reasons to convert.)

**Bottom-up (iterative table)** — the full 2-D form; section 5 is this plus rolling rows:

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]   # init = base cases (all 0)
        for i in range(1, m + 1):                    # loop order: i then j, ascending
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
```

**The mechanical conversion recipe:**

1. **State → params → table index.** The memo key `(i, j)` becomes the 2-D index `dp[i][j]`.
2. **Memo → table.** `@lru_cache` becomes an `(m+1) × (n+1)` array — one cell per state, including the empty-prefix border.
3. **Recursion order → loop order.** Every call moves to smaller `i` and/or `j`, so both loops run ascending — up, left, and diagonal cells are final before they're read.
4. **Base case → initialization.** `if i == 0 or j == 0: return 0` becomes the zero-filled row 0 and column 0.

Then observe the one-row-back dependency and compress to two rows — the 2-row optimization of section 5.

## 9. Interviewer follow-up

- **"Return the subsequence itself."** Keep the full table and backtrack from `(m, n)`: diagonal on match, toward the larger neighbor on mismatch. (This is incompatible with the 2-row compression — a classic trade-off to name out loud.)
- **"Minimum deletions/insertions to make the strings equal?"** `(m - L) + (n - L)` where `L` is the LCS — and generalizing mismatch handling to substitutions gives Edit Distance (72), the natural next problem.
- **"Longest common *substring*?"** Same table, but mismatch sets the cell to 0 and the answer is the max cell anywhere — contiguity changes one line.
- **Diff tools:** `diff` is LCS on lines; mention Hirschberg's algorithm (LCS reconstruction in linear space) or Myers' O(nd) diff if the interviewer pushes on scale.
