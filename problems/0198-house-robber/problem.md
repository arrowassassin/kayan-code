# House Robber

A burglar is casing a street of houses. `nums[i]` is the amount of cash stashed in house `i`. The houses have linked alarms: robbing two **adjacent** houses on the same night trips the system. The burglar may otherwise pick any subset of houses.

Return the maximum total cash obtainable without ever robbing two adjacent houses.

## Example 1

```
Input: nums = [1,2,3,1]
Output: 4
```

Rob houses 0 and 2: `1 + 3 = 4`. Robbing houses 1 and 3 gives only `2 + 1 = 3`.

## Example 2

```
Input: nums = [2,7,9,3,1]
Output: 12
```

Rob houses 0, 2 and 4: `2 + 9 + 1 = 12`.

## Constraints

- `1 <= len(nums) <= 100`
- `0 <= nums[i] <= 400`

A single house is a valid input (rob it). Skipping every house is allowed, so the answer is never negative.
