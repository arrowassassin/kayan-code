## Hint 1

Checking `left.val < node.val < right.val` at each node is not enough — build the tree `[5,4,6,null,null,3,7]` on paper and find the node that passes every local check yet breaks the BST rule against a grandparent.

## Hint 2

Each node isn't constrained by its parent alone but by *every* ancestor it turned left or right under. All those constraints compress into just two numbers: a lower bound and an upper bound that the node's value must lie strictly between.

## Hint 3

Recurse with `(node, low, high)`, starting from `(-∞, +∞)`. Fail if `node.val` is outside the open interval; recurse left with the interval `(low, node.val)` and right with `(node.val, high)`. Strict comparisons everywhere — equal values must be rejected.
