# Number of Islands

You are given a 2-D grid of characters where `"1"` marks land and `"0"` marks water. Count how many islands the grid contains.

An island is a group of land cells connected **horizontally or vertically** (never diagonally), completely surrounded by water or the edge of the grid. You may assume the grid's outside border is all water.

## Example 1

```
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```

The two top-left blocks form one island, the single `1` in the middle is a second, and the pair at bottom-right is a third.

## Example 2

```
Input: grid = [["1"]]
Output: 1
```

## Constraints

- `1 <= m, n <= 300` where `m x n` is the grid size
- `grid[i][j]` is `"1"` or `"0"`

**Note:** you may mutate the grid.
