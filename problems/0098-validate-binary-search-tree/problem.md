# Validate Binary Search Tree

Given the root of a binary tree, decide whether it is a **valid binary search tree** (BST).

A valid BST obeys, at *every* node:

- every value in the node's **left** subtree is **strictly less** than the node's value;
- every value in the node's **right** subtree is **strictly greater** than the node's value;
- both subtrees are themselves valid BSTs.

Note the rule constrains **entire subtrees**, not just direct children — a grandchild can violate the BST property against a distant ancestor even when every parent–child pair looks fine locally.

Return `True` or `False`.

## Example 1

```
Input: root = [2,1,3]

    2
   / \
  1   3

Output: true
```

## Example 2

```
Input: root = [5,1,4,null,null,3,6]

    5
   / \
  1   4
     / \
    3   6

Output: false
```

`4` sits in the right subtree of `5` but is less than `5` — invalid, even though `3 < 4 < 6` locally.

## Constraints

- `0 <= number of nodes <= 10^4` (an empty tree is a valid BST)
- `-2^31 <= Node.val <= 2^31 - 1` — the full 32-bit range, including both extremes
- Equal values are **not** allowed anywhere in a subtree relative to its root (strict inequalities).
