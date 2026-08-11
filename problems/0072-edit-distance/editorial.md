# Edit Distance — Editorial

## 1. Pattern recognition

Two strings, minimize a cost over ways of transforming one into the other — the apex of the **two-string DP** family (LCS 1143 is the warm-up: same table, simpler payload). The tell that this is prefix DP and not search: edits can be reordered so that each operation "resolves" one boundary position, meaning the cheapest transformation of two prefixes is a self-contained subproblem. This recurrence — Levenshtein distance — powers spell checkers, fuzzy search, and DNA alignment, and interviewers grade heavily on whether you can *derive* the three-way choice rather than recite it.

## 2. Brute force first

Search over edit scripts: from `word1`, try every insert/delete/replace, BFS/DFS toward `word2`. The branching factor is enormous (26 letters × positions) and the depth is up to 500 — hopeless. Even the cleaner recursion on string ends branches three ways per mismatch: O(3^(m+n)) ≈ 3^1000 raw calls. But each call is determined by two prefix lengths `(i, j)` alone — at most 501 × 501 ≈ 2.5 × 10^5 distinct subproblems. The entire exponential gap is the same question asked again and again.

## 3. The key insight

**Look at the last characters: if they match, they cost nothing (`dp[i-1][j-1]`); if not, exactly one operation — replace, delete, or insert — resolves that boundary, so `dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])`.**

## 4. Step-by-step derivation

1. **Name the state.** `dist(i, j)` = fewest edits turning `word1[:i]` into `word2[:j]`. An optimal edit script can be normalized to work left-to-right, so once both boundaries pass a point, nothing behind it is touched again — the pair `(i, j)` fully captures the remaining task.
2. **Say the choice out loud.** Consider how an optimal script treats the *last* characters:
   - `word1[i-1] == word2[j-1]`: "match them for free" — `dist(i-1, j-1)`. (Exchange argument: any script that edits a matching pair can be rewritten no worse without doing so.)
   - Otherwise, the script's last effective operation at this boundary is one of exactly three things: **replace** `word1`'s last char with `word2`'s (both prefixes shrink: `dist(i-1, j-1) + 1`), **delete** `word1`'s last char (`dist(i-1, j) + 1`), or **insert** `word2`'s last char at the end (`dist(i, j-1) + 1`). Three cases, exhaustive — take the min.
3. **Base cases:** against an empty string there is only one strategy — `dist(i, 0) = i` (delete all), `dist(0, j) = j` (insert all).
4. **Why memoization collapses the cost:** 3^(m+n) tree nodes, but only (m+1)(n+1) distinct `(i, j)` pairs. Caching makes each pair O(1) → O(m·n) ≈ 2.5 × 10^5 operations. This is the standard exponential→polynomial argument: bound the *state space*, not the call tree.
5. **Space:** each row reads the previous row (`prev[j]`, `prev[j-1]`) and its own left cell (`cur[j-1]`) — two rolling rows, O(min(m, n)) after orienting the shorter string along the columns.

## 5. Annotated Python solution

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        # prev[j] = distance(word1[:i-1], word2[:j])
        prev = list(range(n + 1))          # row 0: j inserts build word2[:j]
        for i in range(1, m + 1):
            cur = [i] + [0] * n            # column 0: i deletes erase word1[:i]
            c1 = word1[i - 1]
            for j in range(1, n + 1):
                if c1 == word2[j - 1]:
                    cur[j] = prev[j - 1]   # ends agree: free
                else:
                    cur[j] = 1 + min(
                        prev[j - 1],       # replace
                        prev[j],           # delete from word1
                        cur[j - 1],        # insert into word1
                    )
            prev = cur
        return prev[n]
```

## 6. Complexity

- **Time O(m · n)** — "one constant-time three-way min per pair of prefixes."
- **Space O(min(m, n))** — "only the previous row is ever read, so two rolling rows over the shorter word."

## 7. Edge-case traps

- **Empty strings** — `("", "")` → 0, `("", "abc")` → 3: the borders *are* the answer; a table initialized to zeros silently returns 0 for everything.
- **Equal strings** → 0 — the free-match diagonal must actually be taken, not min'd against cost-1 options plus one.
- **`"ab"` → `"ba"`** is 2 (two replaces or delete+insert), not 1 — there is no "swap" operation; interviewers use this to check you read the operation set.
- **Off-by-one:** `dp[i][j]` covers prefixes of length `i`/`j`, so characters compared are `word1[i-1]`/`word2[j-1]`.
- **Highly repetitive long inputs** (`"abab..."` vs `"baba..."` → 2): scripts that fix the ends beat character-by-character repair; only the DP finds them.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion)** — the derivation, verbatim:

```python
from functools import lru_cache

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        @lru_cache(maxsize=None)
        def dist(i: int, j: int) -> int:      # edits: word1[:i] -> word2[:j]
            if i == 0:
                return j                      # base: insert all of word2[:j]
            if j == 0:
                return i                      # base: delete all of word1[:i]
            if word1[i - 1] == word2[j - 1]:
                return dist(i - 1, j - 1)     # free match
            return 1 + min(
                dist(i - 1, j - 1),           # replace
                dist(i - 1, j),               # delete
                dist(i, j - 1),               # insert
            )
        return dist(len(word1), len(word2))
```

(Depth can reach m + n = 1000 — close to CPython's recursion limit; another practical vote for bottom-up.)

**Bottom-up (iterative table)** — full 2-D version; section 5 is this with rolling rows:

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i                     # init = base cases
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):            # loop order: both ascending
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j - 1],
                                       dp[i - 1][j],
                                       dp[i][j - 1])
        return dp[m][n]
```

**The mechanical conversion recipe:**

1. **State → params → table index.** Memo key `(i, j)` → table cell `dp[i][j]`, including the `i = 0` / `j = 0` border states.
2. **Memo → table.** `@lru_cache` → an `(m+1) × (n+1)` array sized by the state space.
3. **Recursion order → loop order.** All three recursive calls shrink `i` and/or `j`, so both loops ascend — up, left, and diagonal are final before each cell computes.
4. **Base case → initialization.** The two `if i == 0 / j == 0` returns become the pre-filled first row (`0..n`) and first column (`0..m`).

Final pass: one-row-back dependency → compress to two rows (section 5).

## 9. Interviewer follow-up

- **Weighted operations** (insert ≠ delete ≠ replace cost): replace each `1 +` with the operation's cost — the structure is untouched; note that with replace cost ≥ insert + delete the replace branch goes unused.
- **Only insert/delete allowed?** Distance becomes `m + n − 2·LCS` — tie it back to Longest Common Subsequence (1143), the sibling problem.
- **Return the edit script:** keep the full table, backtrack from `(m, n)` choosing the branch that produced each cell — incompatible with rolling rows; name the trade-off.
- **"Is the distance ≤ k?" for small k** — compute only the diagonal band of width 2k+1 (O(k · min(m,n))), the trick behind fast fuzzy matching; a `-1` outside the band substitutes for missing cells.
