from collections import deque


class Solution:
    def solve(self, board: list[list[str]]) -> None:
        rows, cols = len(board), len(board[0])

        # 1) flood from every border "O": those regions can escape.
        queue = deque()
        for r in range(rows):
            for c in (0, cols - 1):
                if board[r][c] == "O":
                    board[r][c] = "S"       # S = safe
                    queue.append((r, c))
        for c in range(cols):
            for r in (0, rows - 1):
                if board[r][c] == "O":
                    board[r][c] = "S"
                    queue.append((r, c))

        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                    board[nr][nc] = "S"     # mark on enqueue
                    queue.append((nr, nc))

        # 2) one sweep: unreached "O" is captured, "S" is restored.
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "S":
                    board[r][c] = "O"
