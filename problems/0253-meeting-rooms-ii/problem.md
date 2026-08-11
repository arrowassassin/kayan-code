# Meeting Rooms II

You are given a list of meetings, each a half-open time slot `[start, end)` (the room frees up exactly at `end`). Every meeting must be held, and a room can host only one meeting at a time. Return the minimum number of conference rooms needed to run the whole schedule.

Because slots are half-open, a meeting ending at time `t` and another starting at time `t` can share a room.

## Example 1

```
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2
```

`[0,30]` occupies one room the whole time; `[5,10]` and `[15,20]` take turns in a second room.

## Example 2

```
Input: intervals = [[7,10],[2,4]]
Output: 1
```

The meetings never coincide, so one room suffices.

## Constraints

- `1 <= len(intervals) <= 10^5`
- `intervals[i] = [start, end]` with `0 <= start < end <= 10^6`
- The input is not sorted; meetings may be identical
