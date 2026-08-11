# Merge Intervals

You are given a list of closed intervals `intervals`, in **no particular order** and possibly overlapping. Combine every group of overlapping intervals into a single interval and return the resulting list, sorted by start.

Touching intervals (e.g. `[1,4]` and `[4,6]`) count as overlapping and must be combined.

## Example 1

```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
```

`[1,3]` and `[2,6]` overlap, so they collapse into `[1,6]`; the other two stand alone.

## Example 2

```
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
```

They share the endpoint `4`, which counts as overlapping.

## Constraints

- `1 <= len(intervals) <= 10^4`
- `intervals[i] = [start, end]` with `0 <= start <= end <= 10^5`
- The input is **not** guaranteed to be sorted
- Intervals may be nested, duplicated, or degenerate (`start == end`)
