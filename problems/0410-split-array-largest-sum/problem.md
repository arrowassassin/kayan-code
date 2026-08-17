# Split Array Largest Sum

Split the integer array `nums` into exactly `k` non-empty **contiguous** subarrays. Every split has a cost: the largest subarray sum it produces. Return the **minimum possible** value of that largest sum over all valid splits.

## Example 1

```
Input: nums = [7,2,5,10,8], k = 2
Output: 18
```

The best split is `[7,2,5] | [10,8]` with block sums `14` and `18`. Any other cut point leaves a block summing to more than 18 (e.g. `[7,2,5,10] | [8]` costs 24).

## Example 2

```
Input: nums = [1,2,3,4,5], k = 2
Output: 9
```

`[1,2,3] | [4,5]` gives blocks of `6` and `9`.

## Example 3

```
Input: nums = [10,2,3,10], k = 2
Output: 13
```

`[10,2] | [3,10]` with block sums `12` and `13`. Cutting anywhere else leaves a block of 15 or more.

## Constraints

- `1 <= len(nums) <= 5 * 10^4`
- `0 <= nums[i] <= 10^6`
- `1 <= k <= min(50, len(nums))`
- Subarrays must be contiguous and non-empty; every element belongs to exactly one subarray.
