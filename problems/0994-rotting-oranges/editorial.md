# Rotting Oranges — Editorial

## 1. Pattern recognition

The statement's giveaways: a grid, a process that spreads to **edge-adjacent** cells, and the question "how many *minutes* until done". "How many steps until X reaches Y" is the language of **shortest paths in an unweighted graph**, and unweighted shortest path means **BFS** — its layers *are* distances. The twist over Number of Islands (this problem's warmup): rot starts from *several* cells at once, which turns the flood-fill into a **multi-source BFS**. DFS is the wrong tool here — it explores one branch to exhaustion and tells you nothing about *when* each cell was reached.

## 2. Brute force first

Simulate minute by minute: each minute, scan the whole grid, collect the fresh oranges adjacent to a rotten one, flip them, repeat until nothing changes. Each sweep is O(mn) and the process can take up to O(m + n) minutes (rot crossing a 300×300 snake-shaped corridor takes hundreds of minutes — up to ~m·n/2 in the worst layouts), so worst case is O((mn)²) ≈ 8 × 10⁹ steps. Too slow, and wasteful in an obvious way: every sweep re-examines thousands of cells whose fate was already decided.

## 3. The key insight

**Seed one queue with every rotten orange at minute 0; then each BFS layer is exactly one minute of simultaneous spread.**

## 4. Step-by-step derivation

1. Frame the grid as a graph: cells are nodes, edges connect 4-directional neighbors. Rot travels one edge per minute, so "when does this orange rot" = its shortest distance to the *nearest* rotten orange.
2. One BFS per rotten source, taking a min per cell, would work but repeats work. The classic trick: imagine a **virtual super-source** connected to all rotten oranges. BFS from the super-source is just BFS with all rotten cells enqueued up front.
3. Process the queue in layers: snapshot `len(queue)`, pop that many, push their fresh neighbors. Layer `k` rots at minute `k`.
4. Visited-set discipline: mark a fresh orange rotten **when you enqueue it**, not when you pop it — otherwise two neighbors can enqueue the same cell and your layer counts (and runtime) inflate.
5. Track `fresh` as a counter. When the queue drains, `fresh == 0` means the last layer's index is the answer; `fresh > 0` means `-1`. Guard the no-fresh-at-all case before looping so you return `0` instead of running an off-by-one loop.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0

        # seed the queue with EVERY rotten orange at once (minute 0)
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:
            return 0                        # nothing to rot: 0 minutes, not -1

        minutes = 0
        while queue and fresh:
            minutes += 1
            for _ in range(len(queue)):     # one full layer = one minute
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2    # mark on enqueue, not on dequeue
                        fresh -= 1
                        queue.append((nr, nc))

        return minutes if fresh == 0 else -1
```

## 6. Complexity

- **Time O(m·n)** — "every cell is enqueued at most once and each pop does constant work over 4 neighbors."
- **Space O(m·n)** — "in the worst case the queue holds an entire layer, which can be a constant fraction of the grid."

## 7. Edge-case traps

- **No fresh oranges at all** (`[[0,2]]`, `[[0]]`) → must return `0`; a loop that always increments `minutes` returns 1 here.
- **A fresh orange with no rotten anywhere** (`[[1]]`) → `-1`, and your loop must terminate rather than spin.
- **Fresh orange sealed off by zeros** → the `-1` path; this is why you count `fresh` instead of re-scanning.
- **Marking on dequeue instead of enqueue** → duplicate queue entries; answers are still often right, which makes the bug nasty — the stress test's 300×300 grid punishes it.
- **Counting the final empty layer** → off-by-one giving `answer + 1`; the layered loop with the `fresh` guard avoids it.

## 8. Reusable template

Not DP. This trains the **multi-source BFS layer-counting template** — the same skeleton solves Walls and Gates, 01 Matrix, and Shortest Bridge.

## 9. Interviewer follow-up

- *"What if new rotten oranges are dropped in over time?"* — keep the queue alive and append arrivals tagged with their drop minute; BFS order by minute still holds because timestamps are non-decreasing.
- *"Return, for every orange, the minute it rots"* — same BFS, but store the layer index per cell (that's exactly 01 Matrix / Walls and Gates).
- *"Rot spreads diagonally too?"* — swap the 4-neighbor tuple for 8 offsets; nothing else changes, which is worth saying aloud: the template isolates the neighbor rule in one line.
