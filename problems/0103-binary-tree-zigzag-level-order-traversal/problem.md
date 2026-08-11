# Binary Tree Zigzag Level Order Traversal

Given the root of a binary tree, return its values level by level, but with the reading direction **alternating**: the root level reads left-to-right, the next level right-to-left, the one after left-to-right again, and so on.

## Example 1

```
Input: root = [3,9,20,null,null,15,7]

    3
   / \
  9  20
     / \
    15  7

Output: [[3],[20,9],[15,7]]
```

Level 0 reads left-to-right (`[3]`), level 1 right-to-left (`[20,9]`), level 2 left-to-right again (`[15,7]`).

## Example 2

```
Input: root = [1]
Output: [[1]]
```

## Constraints

- `0 <= number of nodes <= 10^4`
- `-1000 <= Node.val <= 1000`
- An empty tree returns `[]`.
- Only the order **within** each inner list alternates — the levels themselves are always listed top to bottom.
