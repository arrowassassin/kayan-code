# Moving Average from Data Stream

Integers arrive one at a time from a stream. Build a class that always knows the average of the **last `size` values seen** (or of all values, while fewer than `size` have arrived). Implement `MovingAverage`:

- `MovingAverage(size)` — fix the window length `size`.
- `next(val) -> float` — consume the next stream value and return the average of the most recent `size` values (including `val`).

Every call to `next` must run in **O(1)** time, and the object may hold at most **O(size)** state — the stream is unbounded, so you cannot keep everything.

## Example

```
MovingAverage m = MovingAverage(3)
m.next(1)     # returns 1.0          window: [1]
m.next(10)    # returns 5.5          window: [1, 10]
m.next(3)     # returns 4.66667      window: [1, 10, 3]
m.next(5)     # returns 6.0          window: [10, 3, 5]  (1 fell out)
```

## Constraints

- `1 <= size <= 1000`
- `-10^5 <= val <= 10^5`
- Up to `10^4` calls to `next`
- Answers are accepted within `1e-6` of the true average
