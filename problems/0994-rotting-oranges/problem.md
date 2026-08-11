# Rotting Oranges

A warehouse grid holds oranges. Each cell of the `m x n` grid contains one of:

- `0` — an empty cell,
- `1` — a fresh orange,
- `2` — a rotten orange.

Every minute, rot spreads: any fresh orange that shares an edge (up, down, left or right) with a rotten orange becomes rotten itself. All spreading in a given minute happens simultaneously.

Return the number of minutes until no fresh orange remains. If some fresh orange can never rot (it is walled off from every rotten one), return `-1`. If there are no fresh oranges to begin with, the answer is `0`.

## Example 1

```
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4
```

The rot ripples out from the top-left corner; the bottom-right orange is the last to turn, at minute 4.

## Example 2

```
Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
```

The orange at row 2, column 0 is sealed off by empty cells — it never rots.

## Example 3

```
Input: grid = [[0,2]]
Output: 0
```

No fresh oranges exist, so zero minutes pass.

## Constraints

- `1 <= m, n <= 300`
- `grid[i][j]` is `0`, `1`, or `2`

Rot spreads only through shared edges, never diagonally. You may mutate the grid.
