# Sliding Window Maximum

You are given an integer array `nums` and a window size `k`. Slide a window of exactly `k` consecutive elements from the left edge of the array to the right edge, one position at a time.

Return a list containing the **maximum** of each window, in order. The result has `len(nums) - k + 1` entries.

## Example 1

```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
```

```
[1  3  -1] -3  5  3  6  7   -> 3
 1 [3  -1  -3] 5  3  6  7   -> 3
 1  3 [-1  -3  5] 3  6  7   -> 5
 1  3  -1 [-3  5  3] 6  7   -> 5
 1  3  -1  -3 [5  3  6] 7   -> 6
 1  3  -1  -3  5 [3  6  7]  -> 7
```

## Example 2

```
Input: nums = [1], k = 1
Output: [1]
```

## Constraints

- `1 <= len(nums) <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `1 <= k <= len(nums)`

An `O(n * k)` solution will exceed the time limit; aim for `O(n)` or `O(n log n)`.
