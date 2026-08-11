# Boundary of Binary Tree

Given the root of a binary tree, return the values on its **boundary**, listed in **anti-clockwise** order starting from the root.

The boundary is the concatenation of four pieces, in this order, with **no node repeated**:

1. **The root.**
2. **The left boundary**: start at the root's left child and repeatedly descend, taking the left child when it exists and the right child otherwise. Stop before any leaf — leaves belong to piece 3, not here. If the root has no left child, this piece is empty.
3. **All leaves**, from left to right. A leaf is a node with no children. The root never counts as a leaf here (a single-node tree contributes its root via piece 1 only).
4. **The right boundary, reversed**: start at the root's right child and repeatedly descend, taking the right child when it exists and the left child otherwise, again excluding leaves — then list this path bottom-up. If the root has no right child, this piece is empty.

Return the concatenated list of values.

## Example 1

```
Input: root = [1,null,2,3,4]

    1
     \
      2
     / \
    3   4

Output: [1,3,4,2]
```

Root = `[1]`. Left boundary is empty (no left child). Leaves = `[3,4]`. Right boundary top-down is `[2]` (node `4` is a leaf, so it is excluded), reversed = `[2]`.

## Example 2

```
Input: root = [1,2,3,4,5,6,7,null,null,8,9]

          1
        /   \
       2     3
      / \   / \
     4   5 6   7
        / \
       8   9

Output: [1,2,4,8,9,6,7,3]
```

Root = `[1]`. Left boundary = `[2]` (its child `4` is a leaf). Leaves = `[4,8,9,6,7]`. Right boundary top-down = `[3]` (`7` is a leaf), reversed = `[3]`.

## Constraints

- `0 <= number of nodes <= 10^4`
- `-1000 <= Node.val <= 1000`
- The tree may be arbitrarily skewed; a chain of `10^4` nodes is a valid input.
- Values are **not** necessarily unique — produce positions, not values, exactly once each.
