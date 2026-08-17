class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int, k: int) -> bool:
            if board[r][c] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            board[r][c] = "#"           # choose: mark used (no char is '#')
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, k + 1):
                    board[r][c] = word[k]   # restore even on the success path
                    return True
            board[r][c] = word[k]       # unchoose: restore before giving up
            return False

        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
