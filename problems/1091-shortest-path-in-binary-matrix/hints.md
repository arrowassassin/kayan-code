## Hint 1

"Shortest path" where every move costs the same (one cell) — which traversal guarantees that the first time you reach a cell, you reached it by a shortest route? What would go wrong if you used DFS here?

## Hint 2

The only twists on the standard grid BFS are: **8 neighbor offsets** instead of 4 (two nested `-1..1` loops, or an explicit list of 8 deltas), and a length counted in *cells*, so the start cell already contributes 1.

## Hint 3

Reject up front if `grid[0][0]` or `grid[n-1][n-1]` is `1`. BFS from `(0,0)` carrying the path length (start at 1), marking cells visited **when enqueued** — overwriting the cell with `1` works as the visited set. Return the length the moment you pop the bottom-right cell; return `-1` if the queue drains. Check the `n = 1` case: a single `0` answers `1`.
