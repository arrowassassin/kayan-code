# Logger Rate Limiter

A logging service receives messages with timestamps (in seconds, arriving in **non-decreasing** order) and must throttle duplicates: a given message text may be printed at most once every **10 seconds**. Implement `Logger`:

- `Logger()` — create the rate limiter.
- `shouldPrintMessage(timestamp, message) -> bool` — return `True` if `message` should be printed at time `timestamp`, otherwise `False`.

A message printed at time `t` blocks every identical message until time `t + 10`; a duplicate arriving exactly at `t + 10` **is** printed. Messages that are *not* printed do **not** reset the timer. Different messages never affect each other.

## Example

```
Logger log = Logger()
log.shouldPrintMessage(1,  "foo")   # True   (first time)
log.shouldPrintMessage(2,  "bar")   # True   (different message)
log.shouldPrintMessage(3,  "foo")   # False  (printed at 1; blocked until 11)
log.shouldPrintMessage(8,  "bar")   # False  (printed at 2; blocked until 12)
log.shouldPrintMessage(10, "foo")   # False  (10 < 1 + 10)
log.shouldPrintMessage(11, "foo")   # True   (11 >= 1 + 10)
```

## Constraints

- `0 <= timestamp <= 10^9`, non-decreasing across calls
- `message` is a non-empty string of at most 30 lowercase letters, digits and spaces
- Up to `10^4` calls to `shouldPrintMessage`
