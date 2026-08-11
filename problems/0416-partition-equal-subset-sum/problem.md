# Partition Equal Subset Sum

Given a list of positive integers `nums`, decide whether it can be split into two groups whose sums are equal. Every element must go to exactly one group.

Return `True` or `False`.

## Example 1

```
Input: nums = [1,5,11,5]
Output: true
```

Split as `[1,5,5]` and `[11]` — both sum to 11.

## Example 2

```
Input: nums = [1,2,3,5]
Output: false
```

Total is 11 (odd) — no equal split can exist.

## Example 3

```
Input: nums = [2,2,3,5]
Output: false
```

Total is 12, but no subset sums to exactly 6.

## Constraints

- `1 <= len(nums) <= 200`
- `1 <= nums[i] <= 100`

All values are strictly positive; a single-element array can never be split.
