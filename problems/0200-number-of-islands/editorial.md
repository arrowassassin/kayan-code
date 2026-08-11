# Number of Islands — Editorial

## 1. Pattern recognition

"Count groups of connected cells in a grid" is the canonical **connected components** problem. The signals: a 2-D grid, a connectivity rule (4-directional), and a question about *how many groups*. Any time you see "islands", "regions", "provinces", or "clusters", your first thought should be *graph traversal over an implicit graph* — the grid **is** the adjacency structure, you never build an explicit graph.

## 2. Brute force first

The truly naive idea — for every land cell, check whether it connects to any previously seen island by re-walking the grid — is O((mn)²): for each of the mn cells you may re-traverse the whole grid. At m = n = 300 that's 8.1 × 10⁹ steps — far past the ~10⁷–10⁸ budget for a 3-second Python limit. The waste is obvious: we re-discover the *same* island once per cell it contains.

## 3. The key insight

**The moment you first touch an island, consume it entirely — then it can never be counted again.**

## 4. Step-by-step derivation

1. Start from the brute force: the redundancy is counting an island once per cell. So make each island cost exactly one "discovery".
2. Scan cells left-to-right, top-to-bottom. When the scan hits a `"1"`, that must be a **never-before-seen** island (any previously seen island would already be consumed). Increment the counter.
3. Immediately flood-fill from that cell — DFS or BFS over the 4 neighbors — marking every reachable `"1"` as visited. Overwriting with `"0"` doubles as the visited set (ask the interviewer whether mutating input is OK; if not, keep a `visited` set of coordinates).
4. Every cell is now touched a constant number of times: once by the scan, once by a flood. Total O(mn).

## 5. Annotated Python solution

```python
class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        count = 0

        def flood(r0: int, c0: int) -> None:
            # iterative DFS: sink every land cell of this island
            stack = [(r0, c0)]
            grid[r0][c0] = "0"          # mark BEFORE pushing, not after popping,
            while stack:                 # or the same cell enters the stack twice
                r, c = stack.pop()
                for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"
                        stack.append((nr, nc))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    flood(r, c)
        return count
```

## 6. Complexity

- **Time O(m·n)** — "every cell is visited once by the outer scan and at most once by a flood-fill."
- **Space O(m·n)** worst case — "the stack can hold the whole grid when it's one giant island; O(min(m,n)) if you BFS instead."

## 7. Edge-case traps

- **Single-cell grid** `[["1"]]` or `[["0"]]` — off-by-one in loops shows up here.
- **All land** — recursion-based DFS hits Python's recursion limit at 300×300 = 90,000 depth. This is exactly why the solution above uses an **explicit stack**; say that out loud, it's a strong signal.
- **Grid of strings, not ints** — comparing to `1` instead of `"1"` silently counts zero islands.
- **Diagonals do not connect** — clarify this before coding; some variants connect 8 ways.
- **Mutating input** — fine here (statement allows it), but *ask*; interviewers probe this.

## 8. (DP section — not applicable)

Not a DP problem. The mechanical skill here is the flood-fill template — the same skeleton solves Surrounded Regions, Pacific Atlantic, and Rotting Oranges.

## 9. Interviewer follow-up

- *"What if islands rot/spread over time?"* → multi-source BFS with a queue seeded by all sources at once (that's Rotting Oranges 994, this problem's linked follow-up).
- *"What if the grid is huge and cells arrive as a stream of `addLand` operations?"* → Union-Find with a count that decrements on merge (Number of Islands II); mention path compression + union by rank for near-O(1) amortized ops.
- *"Count distinct island shapes?"* → canonicalize each flood's path signature and dedupe in a set.
