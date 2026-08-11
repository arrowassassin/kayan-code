# Lowest Common Ancestor of a Binary Tree

Given the root of a binary tree and the values of two nodes `p` and `q` that are guaranteed to exist in it, return the **value** of their lowest common ancestor (LCA): the deepest node that has both `p` and `q` in its subtree.

A node counts as its own ancestor — so if `p` is an ancestor of `q`, the LCA is `p` itself.

All node values in the tree are **unique**, and `p` and `q` are given to you as plain integer values (not node references). The tree is *not* a binary search tree — values carry no ordering information.

## Example 1

```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1

        3
      /   \
     5     1
    / \   / \
   6   2 0   8
      / \
     7   4

Output: 3
```

Nodes `5` and `1` sit in different subtrees of the root, so their LCA is `3`.

## Example 2

```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
```

`4` lives inside `5`'s subtree, so `5` is its own — and therefore the — lowest common ancestor.

## Constraints

- `2 <= number of nodes <= 10^4`
- `-10^9 <= Node.val <= 10^9`, all values unique
- `p != q`, and both values are present in the tree
- The tree can be skewed to a chain of `10^4` nodes.
