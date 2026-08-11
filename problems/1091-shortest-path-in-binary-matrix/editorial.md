# Shortest Path in Binary Matrix — Editorial

## 1. Pattern recognition

"Shortest path", "grid", "every step costs one" — the trifecta for **BFS on an implicit grid graph**. When all edges have equal weight, BFS's layer order *is* distance order, so the first time you touch the target you're done. The two deltas from the vanilla template are cosmetic: the neighborhood is **8-directional** (corners count), and length is measured in **cells, not moves**. Neither changes the algorithm — recognizing that out loud ("this is standard unweighted shortest path; only the neighbor rule and the length convention differ") is the fastest possible start.

## 2. Brute force first

DFS/backtracking that enumerates paths and takes the minimum is exponential — an open n×n grid has astronomically many monotone paths alone, and 8-directional movement adds cycles, so you'd need per-path visited bookkeeping that makes it *both* slow and fiddly. The subtler wrong turn: DFS with memoized "best distance so far per cell" looks polynomial but keeps revisiting cells with improved distances — effectively Bellman-Ford's worst case, O((n²)²) in bad grids. The stress tests (a fully open 100×100 grid and a slalom maze) exist to punish both. BFS gets each cell's true distance the *first* time it touches it.

## 3. The key insight

**In an unweighted graph BFS reaches every node first via a shortest path — so pop-order is distance-order, and the answer is the length carried by the first pop of the target cell.**

## 4. Step-by-step derivation

1. Guard the endpoints: if start or goal is a `1`, no path exists — return `-1` before any traversal. (The `n = 1` grid `[[0]]` must survive this and answer 1.)
2. Seed a deque with `(0, 0, 1)` — length counts the start cell itself. Off-by-one here is the most common wrong submission; anchor on the diagonal example whose answer is 2.
3. Expand with all 8 offsets — the two nested `-1..1` loops harmlessly include `(0,0)` since the origin cell is already marked visited.
4. Visited-set discipline: mark **on enqueue** (overwrite the cell with `1`, doubling the grid as the visited structure — ask permission to mutate, or keep a separate set). Marking on dequeue lets a cell be enqueued up to 8 times; on a dense open grid that's an 8× queue and time blowup.
5. Return `length` at the first pop of `(n-1, n-1)`; a drained queue means the goal is walled off → `-1`. No priority queue, no distance array needed — the FIFO queue *is* the distance ordering.

## 5. Annotated Python solution

```python
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
```

## 6. Complexity

- **Time O(n²)** — "each cell enters the queue at most once and expansion tries a constant 8 neighbors."
- **Space O(n²)** — "the queue can hold a large frontier; visited state reuses the input grid."

## 7. Edge-case traps

- **Blocked start or goal** → `-1` immediately; BFS started from a `1` cell corrupts the visited logic.
- **`n = 1`** → `[[0]]` is 1, `[[1]]` is `-1`; the pop-time goal check handles the start-equals-goal case naturally.
- **Counting moves instead of cells** → off by one on every answer; the 2-cell diagonal example catches it.
- **4-directional habit** — using the old 4-neighbor tuple returns 5 instead of 4 on the ring grid `[[0,0,0],[0,1,0],[0,0,0]]`; diagonals are the whole point of this variant.
- **Mark-on-dequeue** — still correct answers, up to 8× the work; the open 100×100 stress test makes the difference visible.

## 8. Reusable template

Not DP. This trains the **single-source grid BFS with distance carrying template** — the base layer that Rotting Oranges (multi-source) and Word Ladder (implicit non-grid states) both extend.

## 9. Interviewer follow-up

- *"Cells have positive weights now"* — BFS breaks (layers no longer equal cost); switch to **Dijkstra** with a heap keyed on accumulated cost — the template's queue becomes a priority queue and the visited check becomes a settled check.
- *"Speed up long open stretches"* — **A\*** with the Chebyshev distance `max(|dr|, |dc|)` as the heuristic (admissible under 8-directional movement); same code plus a priority key.
- *"You may bulldoze one obstacle"* — add a third state dimension "bulldozes left": BFS over `(r, c, k)` (Shortest Path in a Grid with Obstacles Elimination, 1293); the lesson is that BFS templates extend by growing the state, not the algorithm.
