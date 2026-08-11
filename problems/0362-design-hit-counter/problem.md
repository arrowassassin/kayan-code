# Design Hit Counter

Build a counter that tracks how many "hits" a service received in the trailing **300 seconds**. Timestamps are given in seconds and arrive in **non-decreasing** order across all calls (both kinds). Several hits may share the same timestamp. Implement `HitCounter`:

- `HitCounter()` — create an empty counter.
- `hit(timestamp)` — record one hit at time `timestamp`.
- `getHits(timestamp) -> int` — return the number of hits with a timestamp in `(timestamp - 300, timestamp]`, i.e. strictly newer than 300 seconds ago.

A hit at time `t` is counted by `getHits(t + 299)` but **not** by `getHits(t + 300)`.

## Example

```
HitCounter c = HitCounter()
c.hit(1)
c.hit(2)
c.hit(3)
c.getHits(4)      # returns 3   (hits at 1,2,3 are all within (−296, 4])
c.hit(300)
c.getHits(300)    # returns 4
c.getHits(301)    # returns 3   (the hit at 1 is now exactly 300s old — expired)
```

## Constraints

- `1 <= timestamp <= 2 * 10^9`
- Timestamps across all calls are non-decreasing
- Up to `10^4` total calls to `hit` and `getHits`
- Multiple hits at the same timestamp count individually
