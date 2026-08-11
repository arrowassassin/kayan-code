# Pacific Atlantic Water Flow — Editorial

## 1. Pattern recognition

A grid, a movement rule between adjacent cells, and a reachability question — this is flood-fill territory again (Surrounded Regions is the linked warmup). Two extra signals sharpen it: the question asks about reaching **two different borders**, and reachability is per-cell, so the naive framing runs one traversal per cell. Whenever "can each of many sources reach a fixed target set?" shows up, the expert move is to **flip the direction and traverse once from the target set** — the same border-inward inversion that Surrounded Regions trains, now with an added twist: the edge rule must be reversed too.

## 2. Brute force first

For every cell, DFS/BFS outward following "downhill or level" edges and record which oceans it touches. Each traversal is O(mn), and there are mn cells: O((mn)²) = (200·200)² = 1.6 × 10⁹ steps — dead in Python. The waste is glaring: high cells re-explore the same drainage basins thousands of times. Memoizing "this cell reaches ocean X" is tempting but treacherous — the flow relation isn't a DAG when equal heights allow two-way movement, so naive memoized DFS on a partially finished neighbor is a correctness trap. That's the cue for the cleaner inversion.

## 3. The key insight

**Instead of asking which cells drain to an ocean, start at each ocean's border and climb inland — with the comparison flipped to `neighbor >= current`, one multi-source traversal per ocean finds its entire drainage basin.**

## 4. Step-by-step derivation

1. Water moves `current -> next` when `next <= current`. Reverse every edge: the ocean can "reach" a cell going `border -> inland` when `next >= current`. Reachability along reversed edges from the border equals drainage to that ocean — same paths, walked backwards.
2. The Pacific touches the whole top row and left column: that's a set of sources, not one — so seed a single queue with all of them (multi-source BFS, exactly the Rotting Oranges trick).
3. Run it twice: once with Pacific seeds, once with Atlantic seeds (bottom row + right column), each producing a visited set. No distances are needed, so BFS vs DFS is a coin flip; BFS with a `deque` avoids any recursion-limit conversation for a 40,000-cell basin, so take it.
4. Visited-set discipline: add on enqueue. Cells at ocean corners sit in both seed lists of the *same* ocean (top-left is in the top row and the left column) — seeding via `set(starts)` quietly dedupes.
5. The answer is the set intersection, converted back to `[r, c]` pairs — order free, which is why the judge compares unordered.

## 5. Annotated Python solution

```python
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
```

## 6. Complexity

- **Time O(m·n)** — "two traversals, each visiting a cell at most once."
- **Space O(m·n)** — "two visited sets plus a queue bounded by the grid."

## 7. Edge-case traps

- **Comparison direction** — walking inland it's `>=`, not `<=`; flipping it makes the flat-grid case fail loudly and hilly cases fail subtly.
- **Equal heights** — plateaus flow both ways; an all-equal grid answers *every* cell (the stress test).
- **Single row / single column** — every cell borders both oceans; boundary seeding must not double-count corners or crash on 1-wide grids.
- **`[[1]]`** — the cell is in all four seed lists; answer `[[0,0]]`.
- **Peaks and pits** — a tall ridge reaches both oceans; a walled-in pit reaches neither despite low height. Reachability is about paths, not raw height.

## 8. Reusable template

Not DP. This trains the **inverted multi-source flood-fill template** — seed a traversal from the boundary/target set with the edge rule reversed; the same move powers Surrounded Regions and 01 Matrix.

## 9. Interviewer follow-up

- *"Add a third ocean along a diagonal coastline"* — one more seeded traversal and a three-way set intersection; the template scales linearly in the number of target sets.
- *"Water can also flow through tunnels between listed cell pairs"* — add those pairs as extra adjacency edges (both directions, height rule waived); the grid stops being the whole graph, nothing else changes.
- *"Return the number of cells only, memory-tight"* — replace each set with a bitmask row or reuse two bits per cell in an int matrix; intersection becomes a bitwise AND.
