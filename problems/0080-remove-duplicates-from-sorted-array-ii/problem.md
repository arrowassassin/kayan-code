# Remove Duplicates from Sorted Array II

You are given an integer array `nums` sorted in non-decreasing order. Compress it **in place** so that each distinct value appears **at most twice**, keeping the surviving elements in their original relative order.

Return the number of surviving elements, `k`. After your function returns, the first `k` slots of `nums` must hold exactly the surviving elements; whatever sits in the slots beyond `k` is ignored by the judge.

Do this with **O(1)** extra memory — no building a second list.

## Example 1

```
Input: nums = [1,1,1,2,2,3]
Output: 5, with nums[:5] = [1,1,2,2,3]
```

The third `1` is dropped; everything else survives.

## Example 2

```
Input: nums = [0,0,1,1,1,1,2,3,3]
Output: 7, with nums[:7] = [0,0,1,1,2,3,3]
```

## Constraints

- `1 <= len(nums) <= 3 * 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` is sorted in non-decreasing order
- Only the first `k` positions of the mutated array are checked
