# Sort Colors

An array `nums` holds `n` objects colored red, white, or blue, encoded as the integers `0`, `1`, and `2`. Rearrange the array **in place** so that all `0`s come first, then all `1`s, then all `2`s.

You must not call any library sort. Aim for a **single pass** using **O(1)** extra space. The function returns nothing — the judge inspects the mutated array.

## Example 1

```
Input: nums = [2,0,2,1,1,0]
After: nums = [0,0,1,1,2,2]
```

## Example 2

```
Input: nums = [2,0,1]
After: nums = [0,1,2]
```

## Constraints

- `1 <= len(nums) <= 10^5`
- `nums[i]` is `0`, `1`, or `2`
- Modify `nums` in place; the return value is ignored
