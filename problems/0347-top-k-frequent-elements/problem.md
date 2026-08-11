# Top K Frequent Elements

You are given an integer array `nums` and an integer `k`. Return the `k` values that occur most often in `nums`.

The answer may be returned **in any order**. The test data is constructed so that the set of k most frequent values is unique (there is never a tie for the k-th spot).

## Example 1

```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

`1` appears three times and `2` twice; `3` (once) misses the cut. `[2,1]` would also be accepted.

## Example 2

```
Input: nums = [1], k = 1
Output: [1]
```

## Constraints

- `1 <= len(nums) <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `1 <= k <=` number of distinct values in `nums`
- The k most frequent values are uniquely determined.
