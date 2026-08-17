# N-Queens — Editorial

## 1. Pattern recognition

"Place pieces subject to mutual constraints, return **all** distinct solutions, `n <= 9`" — this is *the* canonical constraint-satisfaction backtracking problem, the one the whole genre is named after. The signals: exhaustive output (not count, not existence), a hard validity rule connecting the choices to each other, and a bound tiny enough that factorial-flavored search is clearly intended (n = 9 means at most 9! = 362,880 row-by-row placements before pruning — nothing). The craft being tested isn't the recursion — it's how you *represent the constraints* so that "is this square safe?" costs O(1).

## 2. Brute force first

Choose 9 of 81 squares: C(81, 9) ≈ 2.6 × 10^11 — dead on arrival. One good idea — **one queen per row**, forced by the rules — collapses the space to nⁿ (each row picks any column), and a second — no repeated columns — collapses it to n! permutations. Even then, the naive version validates each *complete* board in O(n²), and worse, it builds millions of boards that were doomed at row 2. Both fixes come from the same move: check constraints **incrementally, at placement time**, and abandon the row the moment a square is attacked.

## 3. The key insight

**All squares on a "\" diagonal share the same `r - c`, and all squares on a "/" diagonal share the same `r + c` — so three hash sets (columns, r−c, r+c) answer "is this square attacked?" in O(1).**

## 4. Step-by-step derivation

1. Since each row holds exactly one queen, encode a partial solution as `queens[r] = c` — a growing list of column choices. Placing row by row makes row conflicts *impossible by construction*: one constraint eliminated without ever checking it.
2. Column conflicts: a set of used columns. Membership test O(1), add on choose, remove on unchoose.
3. Diagonal conflicts — the trick worth memorizing. Step along a "\" diagonal and both `r` and `c` grow by 1, so `r - c` is invariant; along a "/" diagonal `r` grows while `c` shrinks, so `r + c` is invariant. Each diagonal thus has a unique integer name: `r - c` ranges over `-(n-1) … n-1`, `r + c` over `0 … 2n-2`. Two more sets, and *every* attack test is three O(1) lookups — no scanning earlier queens (the O(n)-per-square alternative), no 2D board at all during search.
4. The recursion is the pure template: for each free column `c` in row `r` — add `c` to `queens` and the three sets (**choose**), recurse into row `r + 1` (**explore**), then remove `c` from all four places (**unchoose**). The unchoose must mirror the choose exactly: forget one of the three set removals and phantom queens keep attacking squares in sibling branches, silently deleting valid solutions.
5. At `r == n` all rows are filled and all constraints held the whole way, so the column list *is* a solution — only then convert it to the string board (`"." * c + "Q" + "." * (n - c - 1)` per row). Building strings only at leaves keeps the hot path allocation-free.

## 5. Annotated Python solution

```python
class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        res = []
        queens = []              # queens[r] = chosen column for row r
        cols = set()             # occupied columns
        diag = set()             # "\" diagonals: r - c is constant along each
        anti = set()             # "/" diagonals: r + c is constant along each

        def backtrack(r: int) -> None:
            if r == n:           # every row placed, constraints held throughout
                res.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
                return
            for c in range(n):
                if c in cols or (r - c) in diag or (r + c) in anti:
                    continue     # attacked -> prune before recursing
                queens.append(c)                        # choose
                cols.add(c); diag.add(r - c); anti.add(r + c)
                backtrack(r + 1)                        # explore
                queens.pop()                            # unchoose: mirror the
                cols.remove(c); diag.remove(r - c); anti.remove(r + c)  # choose exactly

        backtrack(0)
        return res
```

## 6. Complexity

- **Time O(n!)** as the standard loose bound — "row r has at most n − r unattacked columns, so the pruned tree is far smaller than nⁿ; the true count is exponential regardless, which n ≤ 9 is telling you is expected." Each square test is O(1) thanks to the three sets; leaf board construction adds O(n²) per solution.
- **Space O(n)** beyond the output — "the recursion stack, the column list and the three sets each hold at most n entries."

## 7. Edge-case traps

- **Asymmetric choose/unchoose** — removing from `cols` but forgetting `diag` or `anti` (or vice versa) on the way out. The search still runs, just returns *too few* solutions — the hardest kind of bug to spot. Keep the two blocks visually mirrored.
- **A single `diagonals` set for both directions** — `r - c` and `r + c` values collide (e.g. both equal 3), causing false "attacked" verdicts. Two separate sets, always.
- **`n = 2` and `n = 3`** — legitimately zero solutions; the function must return `[]`, not crash or return partial boards.
- **`n = 1`** — one board, `["Q"]`; off-by-ones in the string building (`n - c - 1`) surface here.
- **Checking safety by rescanning `queens`** — correct but O(n) per square; at an interview whiteboard it's the difference between "knows the pattern" and "knows the trick".
- **Building the board eagerly** (mutating a 2D char grid during search) — workable, but now the grid itself is state you must restore; the column list keeps the state minimal.

## 8. (DP section — not applicable)

Not DP. This problem trains the choose→explore→unchoose template at full strength: **constraint sets as O(1) pruning oracles**, with the unchoose step restoring *multiple* pieces of state in lockstep — the same discipline Word Search needs for its visited marks.

## 9. Interviewer follow-up

- *"Just count the solutions"* — N-Queens II (52): drop the board building, return a counter; then note the sets can become three **bitmasks** with shifts (`cols`, `diag << 1`, `anti >> 1` per row) — the classic speedup.
- *"Exploit symmetry"* — mirror boards left-right: search only columns `0 … n//2` in row 0 and reflect, doubling counts (careful with the middle column for odd n).
- *"Some squares are blocked"* — pass a forbidden-square set; it's one more O(1) membership test in the guard, the template untouched — a nice demonstration that constraint sets compose.
- *"Sudoku?"* — Sudoku Solver (37) is the same pattern with three constraint sets per placement (row, column, box) and cells as the choice sequence — worth naming to show you see the family, not the problem.
