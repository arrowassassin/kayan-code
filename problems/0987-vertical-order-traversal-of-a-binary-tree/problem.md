# Vertical Order Traversal of a Binary Tree

Place each node of a binary tree on a grid: the root sits at row `0`, column `0`; a node at `(row, col)` puts its left child at `(row + 1, col - 1)` and its right child at `(row + 1, col + 1)`.

Return the node values grouped by **column**, columns ordered left to right. Within one column, order nodes by **row** (top to bottom); when two nodes share the *same row and the same column*, order those by **value**, ascending. This tie rule makes the output fully deterministic.

## Example 1

```
Input: root = [3,9,20,null,null,15,7]

col:   -1   0    1    2
        9   3
            15   20
                 7

Output: [[9],[3,15],[20],[7]]
```

Column `0` holds `3` (row 0) and `15` (row 2), top to bottom.

## Example 2

```
Input: root = [1,2,3,4,6,5,7]

Output: [[4],[2],[1,5,6],[3],[7]]
```

Nodes `6` (left subtree's right child) and `5` (right subtree's left child) both land on cell `(2, 0)` — same row, same column — so the tie breaks by value: `5` before `6`. Node `1` (row 0) precedes both.

## Constraints

- `0 <= number of nodes <= 10^4`
- `0 <= Node.val <= 1000` (values may repeat)
- Columns can range from `-10^4` to `10^4` on skewed trees.
- Only exact `(row, col)` collisions use the value tie-break — nodes merely sharing a column keep row order.
