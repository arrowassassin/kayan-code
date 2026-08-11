# Binary Tree Right Side View

Imagine standing to the **right** of a binary tree and looking at it side-on. From each depth you can see exactly one node — the rightmost one at that depth. Given the root, return the values you would see, ordered from the top of the tree down.

## Example 1

```
Input: root = [1,2,3,null,5,null,4]

    1        <- see 1
   / \
  2   3      <- see 3
   \   \
    5   4    <- see 4

Output: [1,3,4]
```

## Example 2

```
Input: root = [1,null,3]
Output: [1,3]
```

## Constraints

- `0 <= number of nodes <= 10^4`
- `-100 <= Node.val <= 100`
- An empty tree returns `[]`.
- Careful: the visible node at some depth may sit in the **left** subtree — whenever the right side of the tree is shorter than the left.
