# Path Sum III

Given the root of a binary tree of integers (positive, negative, or zero) and an integer `targetSum`, count the paths whose values sum to `targetSum`.

A path here:

- must travel strictly **downward** (each step goes from a node to one of its children);
- may **start at any node** and **end at any node** below it (or be a single node);
- does not need to touch the root or a leaf.

Return the number of such paths.

## Example 1

```
Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8

        10
       /  \
      5    -3
     / \     \
    3   2     11
   / \   \
  3  -2   1

Output: 3
```

The three paths: `5 → 3`, `5 → 2 → 1`, and `-3 → 11`.

## Example 2

```
Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: 3
```

## Constraints

- `0 <= number of nodes <= 10^4`
- `-10^9 <= Node.val <= 10^9`
- `-10^9 <= targetSum <= 10^9`
- Negative values mean a path's running sum can dip below the target and come back — pruning by "sum exceeded target" is incorrect.
