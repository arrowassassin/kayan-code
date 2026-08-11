# Insert Interval

You are given a list of closed intervals `intervals`, sorted by start and pairwise **non-overlapping**, plus one extra interval `newInterval`. Insert the new interval into the list so that the result is again sorted by start and non-overlapping — merging intervals wherever the insertion causes overlap.

Return the resulting list.

## Example 1

```
Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]
```

`[2,5]` overlaps `[1,3]`, so they merge into `[1,5]`.

## Example 2

```
Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
```

The new interval bridges `[3,5]`, `[6,7]` and `[8,10]` into one.

## Constraints

- `0 <= len(intervals) <= 10^4`
- `intervals[i] = [start, end]` with `0 <= start <= end <= 10^5`
- `intervals` is sorted by start and non-overlapping
- `newInterval = [start, end]` with `0 <= start <= end <= 10^5`

Touching intervals (e.g. `[1,2]` and `[2,3]`) count as overlapping and must merge.
