# Non-overlapping Intervals

Given a list of intervals `intervals` (unsorted, possibly with duplicates), remove as few intervals as possible so that the ones remaining are pairwise non-overlapping. Return that minimum number of removals.

For this problem, intervals that only **touch** do **not** overlap: `[1,2]` and `[2,3]` may both stay.

## Example 1

```
Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
```

Remove `[1,3]`; the remaining `[1,2],[2,3],[3,4]` merely touch, which is allowed.

## Example 2

```
Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
```

Any two of the three copies overlap, so only one may stay.

## Constraints

- `1 <= len(intervals) <= 10^5`
- `intervals[i] = [start, end]` with `-5 * 10^4 <= start < end <= 5 * 10^4`
- The input is not sorted; intervals may be nested or duplicated
