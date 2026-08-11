# Surrounded Regions

You are given an `m x n` board of characters, each either `"X"` or `"O"`. A **region** is a group of `"O"` cells connected horizontally or vertically. A region is **captured** — every one of its cells flipped to `"X"` — if it is completely fenced in by `"X"` cells.

A region that touches the border of the board **cannot** be captured: it has an escape route off the edge.

Modify the board **in place**: flip every captured region's cells to `"X"` and leave every escaping region untouched. Return nothing.

## Example 1

```
Input: board = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","O","X","X"]
]
Output (board after the call): [
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","O","X","X"]
]
```

The three connected `"O"`s in the middle are fenced in and flip. The `"O"` at the bottom sits on the border row and survives.

## Example 2

```
Input: board = [["O"]]
Output (board after the call): [["O"]]
```

A single cell is on the border by definition — nothing flips.

## Constraints

- `1 <= m, n <= 200`
- `board[i][j]` is `"X"` or `"O"`

Connectivity is 4-directional only. You must mutate the given board; the return value is ignored.
