# Diameter of Binary Tree

The **diameter** of a binary tree is the number of **edges** on the longest path between any two nodes in the tree. The path may or may not pass through the root, and it never revisits a node.

Given the root, return the diameter.

## Example 1

```
Input: root = [1,2,3,4,5]

      1
     / \
    2   3
   / \
  4   5

Output: 3
```

The longest path is `4 → 2 → 5` extended through the root: `4 → 2 → 1 → 3` (or `5 → 2 → 1 → 3`), which has 3 edges.

## Example 2

```
Input: root = [1,2]
Output: 1
```

## Constraints

- `0 <= number of nodes <= 10^4`
- `-100 <= Node.val <= 100`
- The answer counts **edges**, not nodes — a single-node (or empty) tree has diameter `0`.
- The longest path may lie entirely inside one subtree, far from the root.
