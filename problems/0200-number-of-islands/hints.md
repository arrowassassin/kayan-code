## Hint 1

Think of the grid as a graph: each land cell is a node, edges connect up/down/left/right neighbors. What graph primitive counts connected groups of nodes?

## Hint 2

Scan every cell. Each time you find a `"1"` you have discovered a *new* island — but only if you make sure you never count another cell of the same island again later. How do you mark a whole island as "seen" the moment you find its first cell?

## Hint 3

From the first cell of an island, flood-fill (DFS or BFS) and overwrite every reachable `"1"` with `"0"` (or add to a visited set). The answer is just the number of times the outer scan triggers a flood-fill.
