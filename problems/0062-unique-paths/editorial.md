# Unique Paths — Editorial

## 1. Pattern recognition

"Count the ways to get from A to B when moves only go right/down" is **grid-path counting DP** — the friendliest member of the 2-D DP family. The tell: movement is monotone (you can never come back), so the grid itself is a DAG and "number of paths to a node = sum of paths to its predecessors". This problem exists in the bank as the on-ramp to its follow-up, Longest Common Subsequence (1143): the *same* 2-D table walk, with "count paths" upgraded to "optimize over paths". Master the table mechanics here where the recurrence is trivial.

## 2. Brute force first

Enumerate paths by recursion: at each cell branch right and down. Correct, but the number of paths *is* the answer — `C(198, 99) ≈ 10^58` at 100×100 — and the naive recursion does work proportional to the number of paths. Even at 20×20 it's ~10^10 calls. But every call is fully described by its cell `(r, c)`: at most 10^4 distinct calls. The rest is duplicated effort — the same cell reached along different histories re-answers the identical question.

## 3. The key insight

**A path can only enter a cell from above or from the left, and those two path families are disjoint — so `paths(r, c) = paths(r-1, c) + paths(r, c-1)`.**

## 4. Step-by-step derivation

1. **Name the state.** `paths(r, c)` = number of distinct paths from the start to cell `(r, c)`. The route taken so far doesn't affect the count of completions — position alone is the state.
2. **Say the choice out loud** — for counting problems the "choice" is the *last move*: "the final step into `(r, c)` was either a down-move from `(r-1, c)` or a right-move from `(r, c-1)`. These cases are disjoint and exhaustive, so I add them." Disjoint + exhaustive is what makes `+` correct — no double counting, nothing missed.
3. **Base cases:** the entire first row and first column have exactly one path (a straight line). Equivalently `paths(0, 0) = 1` with out-of-grid cells contributing 0.
4. **Memoize:** ~10^58 paths collapse to `m·n ≤ 10^4` cached cells, O(1) work each. This is the purest demonstration in the bank of *why* memoization turns exponential into polynomial: distinct states are few even when histories are astronomical.
5. **Compress space:** row `r` reads only row `r-1` and its own left neighbor. Sweep a single array left to right: before assignment `row[j]` still holds the value from the previous row ("from above"), `row[j-1]` is already updated ("from the left") — `row[j] += row[j-1]` does both at once. O(n) space.
6. **The combinatorics closed form:** every path is a word with exactly `m-1` D's and `n-1` R's; choosing where the D's go determines everything. So the answer is `C(m+n-2, m-1)` — `math.comb(m+n-2, m-1)`, O(min(m,n)) multiplications. Mention it; but the DP is what survives contact with follow-ups (obstacles, weights, LCS), where no closed form exists.

## 5. Annotated Python solution

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # row[j] = paths to (current row, column j)
        row = [1] * n                  # first row: one straight-line path each
        for _ in range(1, m):
            for j in range(1, n):
                # row[j] (not yet overwritten) = from above,
                # row[j-1] (already updated)   = from the left
                row[j] += row[j - 1]
        return row[-1]
```

## 6. Complexity

- **Time O(m · n)** — "one addition per cell, each cell computed exactly once."
- **Space O(n)** — "each row depends only on the previous row, so one rolling array suffices." (Closed form: O(min(m, n)) time, O(1) space.)

## 7. Edge-case traps

- **`m = 1` or `n = 1`** → exactly 1 path; the loops must degrade gracefully (they do: nothing to iterate).
- **`1 x 1`** → 1, not 0 — the empty path counts.
- **100 × 100** → ~2.3 × 10^57; in Java/C++ this overflows `long` spectacularly. Say so unprompted — it's a cheap signal of care. Python big ints are exact.
- **Rolling-array direction:** sweeping `j` left→right is load-bearing; right→left would read an already-overwritten "above" value. If you compress, be ready to justify the sweep order.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion):**

```python
from functools import lru_cache

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        @lru_cache(maxsize=None)
        def paths(r: int, c: int) -> int:
            if r == 0 or c == 0:          # base case: first row/column
                return 1
            #      arrived from above  +  arrived from the left
            return paths(r - 1, c) + paths(r, c - 1)
        return paths(m - 1, n - 1)
```

**Bottom-up (iterative table)** — the full 2-D form (section 5 is this, compressed to one row):

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[1] * n for _ in range(m)]      # init: first row & column = 1
        for r in range(1, m):                 # loop order: top to bottom,
            for c in range(1, n):             # left to right
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
        return dp[m - 1][n - 1]
```

**The mechanical conversion recipe:**

1. **State → params → table index.** The memo key `(r, c)` becomes the 2-D index: `paths(r, c)` → `dp[r][c]`.
2. **Memo → table.** `@lru_cache` becomes an `m × n` array — one cell per state.
3. **Recursion order → loop order.** `paths(r, c)` depends on smaller `r` and smaller `c`, so iterate both ascending — every cell's dependencies (up, left) are filled before the cell itself.
4. **Base case → initialization.** `if r == 0 or c == 0: return 1` becomes pre-filling the first row and column with 1 (here: initializing the whole table to 1 and only overwriting the interior).

Then compress: the table is read only one row back → keep a single row (section 5).

## 9. Interviewer follow-up

- **Obstacles** (Unique Paths II, 63): blocked cells contribute 0 paths — set `dp[r][c] = 0` there; the closed form dies instantly, the DP barely notices. This is the standard "why we derived the DP" payoff.
- **Minimum path *sum*** (64): same table walk, `+` between predecessors becomes `min` plus the cell's cost — counting DP and optimization DP are the same skeleton.
- **Two strings instead of a grid** — Longest Common Subsequence (1143), the linked follow-up: index `(i, j)` now means "prefix of each string", and the same up/left/diagonal table mechanics compute an optimum over alignments.
- **"Paths that visit a given cell?"** — multiply paths-to-cell by paths-from-cell-to-corner (count DP composes multiplicatively over waypoints).
