# Pacific Atlantic Water Flow

An island is modeled as an `m x n` grid `heights`, where `heights[r][c]` is the terrain height of cell `(r, c)`. The **Pacific** ocean hugs the island's top and left edges; the **Atlantic** hugs the bottom and right edges.

Rain landing on a cell flows to any of its 4-directionally adjacent cells whose height is **less than or equal to** the current cell's height, and it may keep flowing cell to cell under the same rule. Water that reaches any cell on an ocean's border spills into that ocean.

Return the coordinates `[r, c]` of every cell from which rainwater can reach **both** oceans. Cells may be listed in any order.

## Example 1

```
Input: heights = [
  [1,2,2,3,5],
  [3,2,3,4,4],
  [2,4,5,3,1],
  [6,7,1,4,5],
  [5,1,1,2,4]
]
Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

From `(2,2)` (height 5) water can step down-left to reach the Pacific and down-right to reach the Atlantic.

## Example 2

```
Input: heights = [[1]]
Output: [[0,0]]
```

The single cell borders both oceans.

## Constraints

- `1 <= m, n <= 200`
- `0 <= heights[r][c] <= 10^5`

Flow requires `next <= current` — water can move across equal heights, never uphill.
