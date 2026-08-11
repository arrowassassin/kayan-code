# Moving Average from Data Stream — Editorial

## 1. Pattern recognition

"Values arrive one at a time", "last `size` values", "O(1) per call, O(size) state" — this is the entry point of the **stream-processing class design** family (the Snowflake-reported pattern). The tell is the pair of budgets stated up front: a *per-operation* time budget and a *bounded-state* budget against an *unbounded* input. Every design in this family is judged the same way: name the per-op cost of each method before you write it, then make the data structure enforce it.

## 2. Brute force first

Append every incoming value to a list and, on each `next`, sum the last `size` entries: O(size) per call and — worse — O(n) memory for a stream of n values. At 10⁴ calls × window 1000 that's 10⁷ additions, which still runs; the real failure is the unbounded memory on an unbounded stream. The statement's "O(size) state" clause exists precisely to disqualify this: in an interview, the moment you say "I'll keep the whole stream" you've missed the point of the exercise.

## 3. The key insight

**Between two consecutive calls the window changes by exactly one arrival and at most one departure, so the sum can be updated incrementally instead of recomputed.**

## 4. Step-by-step derivation

1. The average is `sum / count`; `count` is trivial (`min(calls, size)`), so the whole problem is maintaining `sum`.
2. When `val` arrives: `sum += val`. When the window exceeds `size`, the *oldest* value leaves: `sum -= oldest`. That's the entire delta.
3. So you need O(1) access to the oldest value — FIFO order. A `deque` gives `append` / `popleft` in O(1); a fixed array of length `size` with a wrapping write index (a **ring buffer**) does the same with zero allocation after construction: `sum -= buf[i]; buf[i] = val; i = (i + 1) % size`.
4. Before the window fills, nothing leaves — divide by the current length, not by `size`. The deque version gets this for free from `len(window)`.
5. Result: one append, at most one evict, one division → O(1) per `next`, O(size) space, independent of stream length.

This eager-evict-on-arrival idiom is the *count-based* window. The follow-up (Design Hit Counter) swaps in a *time-based* window, where eviction is driven by timestamps instead of the element count — same skeleton, different eviction test.

## 5. Annotated Python solution

```python
from collections import deque


class MovingAverage:
    def __init__(self, size: int):
        self.size = size
        self.window = deque()       # holds at most `size` values -> O(size) state
        self.total = 0              # running sum: the whole trick

    def next(self, val: int) -> float:
        self.window.append(val)
        self.total += val
        if len(self.window) > self.size:      # window overflowed by exactly one
            self.total -= self.window.popleft()
        return self.total / len(self.window)  # len, not size: warm-up phase
```

## 6. Complexity

- **Time O(1)** per `next` — "one append, at most one popleft, one division; nothing depends on how many values have streamed by."
- **Space O(size)** — "the deque never exceeds `size` elements; the stream's length never touches memory."

## 7. Edge-case traps

- **`size = 1`** — every call evicts; the answer is always just `val` as a float.
- **Warm-up phase** — dividing by `size` instead of the current count is *the* classic bug (`next(4)` on a size-3 window must return 4.0, not 1.33).
- **Integer division** — in languages other than Python 3, `sum / count` truncates; say "float division" out loud.
- **Negative values and a zero-sum window** — the running sum passing through 0 is fine, but tests will check you didn't special-case it.
- **Floating-point drift** — with int inputs the running sum is exact in Python; mention that with float inputs a long-lived running sum accumulates error (Kahan summation or periodic resummation fixes it).

## 8. (DP section — not applicable)

Not DP. The reusable template: **bounded FIFO window + incrementally maintained aggregate** — the skeleton every time-window design (Hit Counter, rate limiters, sliding-window metrics) is built on.

## 9. Interviewer follow-up

- *"Window by time instead of by count"* — that is Design Hit Counter 362, the linked extension: evict by timestamp comparison rather than length, and decide between a deque of events and O(1)-space circular buckets.
- *"Also report min/max of the window"* — sum is invertible (subtract the leaver), min/max are not; you need a monotonic deque — this is Sliding Window Maximum 239 in stream form.
- *"Millions of concurrent streams"* — the ring buffer wins: fixed `size`-slot array per stream, no per-call allocation; a single stream's `next` is a two-word update, but note the read-modify-write on `total` needs a lock or atomics once producers are concurrent.
- *"Average over the last N seconds instead of N values"* — combine both windows: a deque of `(timestamp, value)` pairs evicted by age, running sum as here.
