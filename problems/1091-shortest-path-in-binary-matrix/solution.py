from collections import deque


class Solution:
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        n = len(grid)
        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
            return -1                       # blocked endpoint: no path at all

        queue = deque([(0, 0, 1)])          # (row, col, path length in cells)
        grid[0][0] = 1                      # reuse the grid as the visited set
        while queue:
            r, c, length = queue.popleft()
            if r == n - 1 and c == n - 1:
                return length
            for dr in (-1, 0, 1):           # all 8 directions
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                        grid[nr][nc] = 1    # mark on enqueue
                        queue.append((nr, nc, length + 1))
        return -1
