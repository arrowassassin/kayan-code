# Word Search — Editorial

## 1. Pattern recognition

A grid, four-directional movement, "may a path exist?" — the skeleton is grid DFS, the same walk as Number of Islands (200). The extra ingredients that turn it into backtracking: the path must spell a **specific sequence**, and a cell is off-limits only **within the current attempt**. That second clause is the whole problem. Flood-fill marks cells visited permanently because "reachable" is monotone — once wet, always wet. "Used by *this* trace" is not monotone, so every mark must be **undone** when the attempt that made it retreats. The bounds (6×6 board, word ≤ 12) are the usual backtracking wink: the search is exponential in the word length and that's intended.

## 2. Brute force first

Enumerate every simple path of length `len(word)` from every start cell, then compare each to the word: the path count alone is astronomically redundant. The natural refinement — extend a path only while it still matches the word prefix — *is* the intended algorithm; there's no cleverer asymptotic waiting behind it. Where implementations actually go wrong is state handling: a shared visited set that never gets cleaned (wrong answers), a fresh visited set copied per call (correct but O(path) per step), or — the classic — marks that are made but never unmade. The brute-force-to-optimal journey here is about *discipline*, not asymptotics.

## 3. The key insight

**A cell is only "used" for the lifetime of the current attempt — mark it on the way in, and restore it on every way out, so sibling and later attempts see a clean board.**

## 4. Step-by-step derivation

1. Define `dfs(r, c, k)`: "can `word[k:]` be traced starting at `(r, c)`?" The answer for the whole problem is whether `dfs(r, c, 0)` holds for any start cell.
2. Order the checks for fail-fast pruning: if `board[r][c] != word[k]`, this branch dies immediately — most calls end right here, which is what keeps the search tractable. If the character matches and `k` is the last index, succeed before doing any marking.
3. **Choose**: overwrite `board[r][c]` with `'#'`. Since no input character is `'#'`, any neighbor stepping back onto this cell fails the character test of step 2 automatically — the mark *is* the visited check. Mutating the board beats a `visited` set here: no extra structure, and the restore is a single assignment. (A set works too — as long as you `discard` on exit; the bug is the missing removal, not the choice of structure.)
4. **Explore**: recurse into the four in-bounds neighbors with `k + 1`. Any success propagates `True` up immediately.
5. **Unchoose**: write `word[k]` back — on the failure path *and* before returning on the success path. The failure-path restore is correctness-critical: a failed attempt through cell X must not leave X poisoned, because a *different* attempt (other start, other route) may legitimately need X. Miss it and the board [["C","A","A"],["A","A","A"],["B","C","D"]] with word "AAB" comes back `False` — the first doomed exploration eats the A's a later trace needs. The success-path restore is politeness (don't hand the caller a vandalized board), and the judge's repeated-call setting makes politeness mandatory.
6. Contrast with 0200 one last time, because interviewers probe exactly this: islands never un-mark (monotone knowledge: "this cell is water/visited"), word search always un-marks (attempt-scoped knowledge: "this cell is on *my current* path"). Knowing *which kind of DFS you are writing* is the transferable skill.

## 5. Annotated Python solution

```python
class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int, k: int) -> bool:
            if board[r][c] != word[k]:  # fail fast: most calls die here
                return False
            if k == len(word) - 1:      # matched the final character
                return True
            board[r][c] = "#"           # choose: '#' matches no letter,
                                        # so the mark IS the visited check
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, k + 1):
                    board[r][c] = word[k]   # restore even when succeeding
                    return True
            board[r][c] = word[k]       # unchoose: failed attempts must
            return False                # leave the board exactly as found

        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

## 6. Complexity

- **Time O(m · n · 3^L)** where `L = len(word)` — "every cell can start an attempt, and each step has at most 3 live directions since you never step back onto the cell you came from; exponential in the word, which the 6×6 / length-12 bounds are telling you is fine."
- **Space O(L)** — "the recursion stack is at most the word length; marking in place costs nothing extra."

## 7. Edge-case traps

- **Missing the failure-path restore** — the defining bug, and a hidden test targets it: `[["C","A","A"],["A","A","A"],["B","C","D"]]` / `"AAB"` must be `True`, but stale marks from the first failed exploration block the valid trace.
- **Marking before the character check** (or restoring after an early `return True` is skipped) — order the three phases exactly: check, mark, recurse, restore.
- **A board of one repeated letter** — `6×6` of `'A'` with `"AAAAAAAAAAAB"`: every attempt runs long and fails; without the fail-fast character test up front this is where sloppy versions crawl. The all-`'A'` word of length 12 must still come back `True`.
- **Word longer than the cell count or needing a cell twice** — `"AAAAA"` on a 2×2 of `'A'` is `False`; the no-revisit rule, not the letter supply, is the limit.
- **Case sensitivity** — `'a'` ≠ `'A'`; don't normalize.
- **1×1 boards and single-row/column snakes** — boundary arithmetic in the neighbor loop shows up here first.

## 8. (DP section — not applicable)

Not DP (the subproblem "can `word[k:]` start at `(r,c)`?" depends on the path taken, so it doesn't memoize). This problem trains the choose→explore→unchoose template in its **mutate-the-world** form: the state being restored is the input itself, and the restore must fire on every exit path.

## 9. Interviewer follow-up

- *"Search many words at once"* — Word Search II (212): one DFS per word re-walks shared prefixes; hang all words on a **trie** and walk board and trie together, pruning whole word-families the moment a prefix dies.
- *"Cheap rejections before searching?"* — count letters: if `word` needs more of some character than the board holds, return `False` immediately; also start from the rarer end of the word (reverse it if its last letter is rarer than its first) to shrink the branching early.
- *"Board is huge but the word is short"* — the complexity is dominated by `3^L`, not the grid; index cell positions by character so only matching start cells spawn attempts.
- *"Allow diagonal moves / allow revisits"* — diagonals: grow the neighbor tuple to 8, template unchanged. Revisits allowed: the visited discipline disappears entirely and it degenerates to BFS over (cell, index) states — worth saying, because it shows you know *why* the un-marking existed.
