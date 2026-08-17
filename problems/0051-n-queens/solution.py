class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        res = []
        queens = []                 # queens[r] = column of the queen in row r
        cols = set()                # occupied columns
        diag = set()                # occupied "\" diagonals, keyed by r - c
        anti = set()                # occupied "/" diagonals, keyed by r + c

        def backtrack(r: int) -> None:
            if r == n:
                res.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
                return
            for c in range(n):
                if c in cols or (r - c) in diag or (r + c) in anti:
                    continue        # attacked: prune this column
                queens.append(c)                    # choose
                cols.add(c); diag.add(r - c); anti.add(r + c)
                backtrack(r + 1)                    # explore
                queens.pop()                        # unchoose
                cols.remove(c); diag.remove(r - c); anti.remove(r + c)

        backtrack(0)
        return res
