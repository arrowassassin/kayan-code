# Subarrays with K Different Integers

Given an integer array `nums` and an integer `k`, count the contiguous subarrays of `nums` that contain **exactly** `k` distinct values.

Two subarrays are counted separately whenever their index ranges differ, even if their contents are equal.

## Example 1

```
Input: nums = [1,2,1,2,3], k = 2
Output: 7
```

The qualifying subarrays are `[1,2]`, `[2,1]`, `[1,2]`, `[2,3]`, `[1,2,1]`, `[2,1,2]`, `[1,2,1,2]`.

## Example 2

```
Input: nums = [1,2,1,3,4], k = 3
Output: 3
```

They are `[1,2,1,3]`, `[2,1,3]`, `[1,3,4]`.

## Constraints

- `1 <= len(nums) <= 2 * 10^4`
- `1 <= nums[i], k <= len(nums)`

The count fits in a 64-bit integer (Python ints are unbounded).
