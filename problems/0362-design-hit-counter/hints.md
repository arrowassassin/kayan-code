## Hint 1

This is Moving Average's window turned from *count-based* into *time-based*: a hit stops mattering not after N more hits arrive, but after 300 seconds pass. What decides when an old record can be thrown away?

## Hint 2

Timestamps are non-decreasing, so the recorded hits are already sorted by time. The stale ones always form a prefix. Keep the hits in a queue and, whenever a call comes in at time `t`, pop from the front while the front's timestamp is `<= t - 300`. Each hit is pushed once and popped at most once — the eviction loop is amortized O(1).

## Hint 3

Two refinements: (a) many hits can share a timestamp — store `(timestamp, count)` pairs and keep a running total so `getHits` doesn't sum the queue; (b) for O(1) *worst-case* space, replace the queue with 300 circular buckets — `buckets[t % 300]` holds `(last_timestamp, count)`, reset when a new timestamp claims the slot, and `getHits` sums the ≤300 buckets whose stored timestamp is still in the window.
