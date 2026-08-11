# Fruit Into Baskets

You are walking down a row of fruit trees. The array `fruits` gives the fruit type of each tree, in order. You carry exactly **two baskets**, and each basket can hold unlimited fruit — but only of a **single type**.

Starting at a tree of your choice, you walk right, picking one fruit from *every* tree you pass. You must stop the moment you reach a tree whose type doesn't fit in either basket.

Return the maximum number of fruits you can collect.

(In plain terms: find the longest contiguous subarray of `fruits` that contains at most **two distinct** values.)

## Example 1

```
Input: fruits = [1,2,1]
Output: 3
```

Both baskets suffice for types 1 and 2 — take all three trees.

## Example 2

```
Input: fruits = [1,2,3,2,2]
Output: 4
```

Start at the second tree: `[2,3,2,2]` uses only types 2 and 3.

## Example 3

```
Input: fruits = [0,1,2,2]
Output: 3
```

`[1,2,2]` beats `[0,1]`.

## Constraints

- `1 <= len(fruits) <= 10^5`
- `0 <= fruits[i] < len(fruits)`
