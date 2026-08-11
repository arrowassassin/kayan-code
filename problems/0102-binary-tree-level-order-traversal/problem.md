# Binary Tree Level Order Traversal

Given the root of a binary tree, return its values grouped **level by level**: the first inner list holds the root, the second holds depth-1 nodes from left to right, and so on down to the deepest level.

## Example 1

```
Input: root = [3,9,20,null,null,15,7]

    3
   / \
  9  20
     / \
    15  7

Output: [[3],[9,20],[15,7]]
```

## Example 2

```
Input: root = [1]
Output: [[1]]
```

## Constraints

- `0 <= number of nodes <= 10^4`
- `-1000 <= Node.val <= 1000`
- An empty tree returns `[]` (not `[[]]`).
- The tree may be completely skewed — a chain of `10^4` nodes yields `10^4` levels of one value each.
