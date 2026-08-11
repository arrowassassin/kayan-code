# Kth Largest Element in an Array

Given an integer array `nums` and an integer `k`, return the `k`-th largest value in the array **counting duplicates** — i.e. the element that would sit at index `k-1` if the array were sorted in descending order. It is *not* the k-th distinct value.

Can you do better than sorting the whole array?

## Example 1

```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
```

Sorted descending: `[6,5,4,3,2,1]` — the 2nd entry is `5`.

## Example 2

```
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

Descending order is `[6,5,5,4,3,3,2,2,1]`; duplicates count, so the 4th largest is `4` (not `3`).

## Constraints

- `1 <= k <= len(nums) <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- Duplicates may appear; they each occupy their own rank.
