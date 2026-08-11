from collections import deque


class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        rows, cols = len(heights), len(heights[0])

        def reachable(starts: list[tuple[int, int]]) -> set[tuple[int, int]]:
            # BFS *inland from the ocean*: climb edges where next >= current
            seen = set(starts)
            queue = deque(starts)
            while queue:
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (0 <= nr < rows and 0 <= nc < cols
                            and (nr, nc) not in seen
                            and heights[nr][nc] >= heights[r][c]):
                        seen.add((nr, nc))
                        queue.append((nr, nc))
            return seen

        pacific = reachable([(0, c) for c in range(cols)]
                            + [(r, 0) for r in range(rows)])
        atlantic = reachable([(rows - 1, c) for c in range(cols)]
                             + [(r, cols - 1) for r in range(rows)])
        return [[r, c] for r, c in pacific & atlantic]
