# Merge K Sorted Lists

You are given an array `lists` containing `k` singly linked lists, each already sorted in non-decreasing order. Combine all of them into one sorted linked list and return its head.

Some of the `k` lists (or all of them, or the array itself) may be empty.

## Example 1

```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
```

Interleaving the three sorted chains produces one sorted chain of all 8 nodes.

## Example 2

```
Input: lists = []
Output: []
```

No lists at all — return an empty list.

## Constraints

- `0 <= k <= 10^4`
- The total number of nodes across all lists is at most `10^5`
- `-10^4 <= node.val <= 10^4`
- Each individual list is sorted in non-decreasing order and has length `0` to `500`
