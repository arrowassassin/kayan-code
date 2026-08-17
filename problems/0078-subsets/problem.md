# Subsets

Given a list `nums` of **distinct** integers, return every possible subset (the power set) — including the empty subset and `nums` itself.

The subsets may appear in **any order**, and the elements inside a subset may appear in any order, but no subset may appear twice.

## Example 1

```
Input: nums = [1,2,3]
Output: [[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]]
```

Eight subsets: every element is independently in or out, so 2^3 = 8.

## Example 2

```
Input: nums = [0]
Output: [[],[0]]
```

## Constraints

- `1 <= len(nums) <= 10`
- `-10 <= nums[i] <= 10`
- All values in `nums` are distinct

Note the tiny bound on `len(nums)` — the output itself has `2^n` entries, so an exponential algorithm is not just acceptable, it is unavoidable.
