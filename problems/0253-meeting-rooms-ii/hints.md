## Hint 1

The answer is the peak number of meetings running at the same instant. You don't need to decide *which* room each meeting goes into — only how many overlap at the busiest moment.

## Hint 2

Process meetings in start order. When a meeting begins, the only question is: has some earlier meeting already ended? You always want to compare against the meeting that ends **soonest** — which structure hands you the minimum end time in O(log n)?

## Hint 3

Two equivalent implementations, know both: (a) sort by start, keep a min-heap of end times; if the heap top `<= start`, replace it (reuse a room), else push (new room) — the final heap size is the answer. (b) Sweep line: turn each meeting into `(start, +1)` and `(end, -1)` events, sort, and track the running sum's maximum. In both, ties at the same timestamp must free the room *before* seating the new meeting.
