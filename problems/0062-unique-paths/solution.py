class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # row[j] = number of paths to the cell in the current row, column j.
        # First row: only one way anywhere (keep going right).
        row = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                # paths from above (row[j], stale value) + from the left (row[j-1])
                row[j] += row[j - 1]
        return row[-1]
