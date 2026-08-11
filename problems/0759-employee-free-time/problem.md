# Employee Free Time

You are given `schedule`, a list of employees' working calendars. Each employee's calendar is a list of closed intervals `[start, end]`, sorted by start and non-overlapping *within that employee*. Different employees' intervals may overlap arbitrarily.

Return the list of **finite** time intervals during which *every* employee is simultaneously free, sorted by start. Ignore the unbounded stretches before the first meeting and after the last one. Zero-length gaps don't count: if one interval ends exactly when another starts, nobody was free in between.

## Example 1

```
Input: schedule = [[[1,2],[5,6]], [[1,3]], [[4,10]]]
Output: [[3,4]]
```

Someone is working during `[1,3]` and during `[4,10]`; the only shared idle window is `[3,4]`.

## Example 2

```
Input: schedule = [[[1,3],[6,7]], [[2,4]], [[2,5],[9,12]]]
Output: [[5,6],[7,9]]
```

## Constraints

- `1 <= len(schedule) <= 50` employees
- `1 <= len(schedule[i]) <= 2000`, at most `2 * 10^4` intervals in total
- Each interval is `[start, end]` with `0 <= start < end <= 10^5`
- Each employee's own list is sorted by start and non-overlapping (but two employees' intervals may touch, nest, or duplicate each other)
