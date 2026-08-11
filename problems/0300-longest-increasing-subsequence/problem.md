# Longest Increasing Subsequence

Given an integer array `nums`, return the length of its longest **strictly increasing** subsequence.

A subsequence keeps the original left-to-right order but may drop any elements — the kept elements do not need to be contiguous. "Strictly" means equal neighbors are not allowed in the subsequence.

## Example 1

```
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
```

One longest increasing subsequence is `[2,3,7,101]` (also `[2,5,7,18]` works — only the length is asked).

## Example 2

```
Input: nums = [0,1,0,3,2,3]
Output: 4
```

`[0,1,2,3]`.

## Example 3

```
Input: nums = [7,7,7,7]
Output: 1
```

Strictly increasing — duplicates cannot extend a run.

## Constraints

- `1 <= len(nums) <= 2500`
- `-10^4 <= nums[i] <= 10^4`

An O(n^2) solution is accepted; can you do O(n log n)?
