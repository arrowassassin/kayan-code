# Minimum Size Subarray Sum

Given an array `nums` of **positive** integers and a positive integer `target`, find the length of the shortest contiguous subarray whose sum is greater than or equal to `target`. If no subarray reaches `target`, return `0`.

## Example 1

```
Input: target = 7, nums = [2,3,1,2,4,3]
Output: 2
```

`[4,3]` sums to 7; no shorter subarray reaches 7.

## Example 2

```
Input: target = 4, nums = [1,4,4]
Output: 1
```

A single `4` suffices.

## Example 3

```
Input: target = 11, nums = [1,1,1,1,1,1,1,1]
Output: 0
```

The whole array sums to 8 — no subarray qualifies.

## Constraints

- `1 <= target <= 10^9`
- `1 <= len(nums) <= 10^5`
- `1 <= nums[i] <= 10^4`

Every element is strictly positive — this matters for which techniques are valid.
