# Shortest Path in Binary Matrix

You are given an `n x n` grid of `0`s and `1`s. A **clear path** runs from the top-left cell `(0, 0)` to the bottom-right cell `(n-1, n-1)` such that:

- every cell on the path is `0`, and
- consecutive cells on the path are adjacent in any of the **8 directions** (sharing an edge *or* a corner).

The **length** of a path is the number of cells it visits, including both endpoints.

Return the length of the shortest clear path, or `-1` if none exists (including when the start or end cell is a `1`).

## Example 1

```
Input: grid = [[0,1],[1,0]]
Output: 2
```

One diagonal hop: `(0,0) -> (1,1)`.

## Example 2

```
Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
Output: 4
```

Slide along the top and down the right edge: 4 cells.

## Example 3

```
Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
Output: -1
```

The start cell is blocked.

## Constraints

- `1 <= n <= 100`
- `grid[i][j]` is `0` or `1`

For `n = 1`, a lone `0` cell is a path of length `1`.
