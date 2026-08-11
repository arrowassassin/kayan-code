# Unique Paths

A robot sits in the top-left cell of an `m x n` grid and wants to reach the bottom-right cell. At every step it may move only **right** or **down** by one cell.

Return the number of distinct paths from the top-left to the bottom-right corner.

## Example 1

```
Input: m = 3, n = 7
Output: 28
```

Every path is a sequence of 2 downs and 6 rights in some order.

## Example 2

```
Input: m = 3, n = 2
Output: 3
```

The three paths: Down-Down-Right, Down-Right-Down, Right-Down-Down.

## Constraints

- `1 <= m, n <= 100`

A `1 x 1` grid has exactly one path (stand still). Answers can be astronomically large (about 10^58 at 100 x 100) — Python integers handle this natively; in other languages you would discuss overflow.
