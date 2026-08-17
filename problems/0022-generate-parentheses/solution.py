class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res = []
        path = []

        def backtrack(opened: int, closed: int) -> None:
            if len(path) == 2 * n:
                res.append("".join(path))
                return
            if opened < n:                # may still open
                path.append("(")
                backtrack(opened + 1, closed)
                path.pop()
            if closed < opened:           # a ')' must have a '(' to match
                path.append(")")
                backtrack(opened, closed + 1)
                path.pop()

        backtrack(0, 0)
        return res
