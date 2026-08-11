# 3Sum

Given an integer array `nums`, return **all unique triplets** `[a, b, c]` of values from the array (three distinct positions) such that `a + b + c == 0`.

The answer must not contain duplicate triplets: two triplets are duplicates if they contain the same three values, regardless of order or which positions they came from. Triplets may be returned in any order, and the values within each triplet may be in any order.

## Example 1

```
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
```

`(-1) + (-1) + 2 = 0` and `(-1) + 0 + 1 = 0`. Note `[-1,0,1]` appears once even though two different `-1` positions could produce it.

## Example 2

```
Input: nums = [0,1,1]
Output: []
```

No three values sum to zero.

## Example 3

```
Input: nums = [0,0,0]
Output: [[0,0,0]]
```

## Constraints

- `0 <= len(nums) <= 3000`
- `-10^5 <= nums[i] <= 10^5`
- The same array position may not be used twice within a triplet, but equal *values* at different positions are fine
