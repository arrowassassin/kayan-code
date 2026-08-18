# Design Hit Counter — Editorial

## 1. Pattern recognition

"Count events in the trailing 300 seconds", non-decreasing timestamps, a class with per-call budgets — this is the **time-based sliding window**, the direct sequel to Moving Average (this problem's warmup). There the window was "last N *values*"; here it is "last 300 *seconds*", so eviction is triggered by timestamp comparison, not by length. This time/count duality is the core idiom of the stream-design family, and interviewers deliberately pick one after the other to see whether you recognize the shared skeleton: bounded state + evict-stale-prefix + maintained aggregate.

## 2. Brute force first

Append every hit's timestamp to a list; `getHits(t)` scans the whole list counting entries in `(t - 300, t]`. That is O(n) per query and O(n) memory forever — a hit from an hour ago is still being touched by every query. With 10⁴ calls it's ~10⁸ comparisons in the worst interleaving (borderline), but the disqualifying flaw is state that grows with total traffic rather than with the window. A stream design that never forgets is wrong by construction.

## 3. The key insight

**Because timestamps arrive in order, the expired hits are always a contiguous prefix of what you stored — so a queue plus a "pop while stale" loop retires each hit exactly once.**

## 4. Step-by-step derivation

1. Hits arrive time-sorted, so store them in arrival order: a deque. The window predicate is `ts > t - 300`; everything failing it sits at the front.
2. On any call at time `t`, `popleft` while `front <= t - 300`. A hit is pushed once and popped at most once, so eviction is **amortized O(1)** per call — one call may pop 300 entries, but only because 300 earlier calls each pushed one. Say "amortized" out loud and give that token argument; it's what the interviewer is fishing for.
3. `getHits` shouldn't count the queue (that's O(window) again): maintain a running `total`, incremented on push, decremented on evict — the same maintained-aggregate move as Moving Average's running sum.
4. Many hits can share one second: compress to `(timestamp, count)` pairs. Now memory is O(distinct seconds in window) ≤ O(300) rather than O(hits in window).
5. The **bucket alternative** removes the queue entirely: 300 circular buckets, `i = t % 300`, each holding `(last_ts, count)`. On `hit(t)`: if `buckets[i].last_ts != t`, the slot belongs to a second ≥300s old — reset it to `(t, 0)` — then increment. On `getHits(t)`: sum `count` over the ≤300 buckets with `last_ts > t - 300`. That's O(1) hit / O(300)=O(1) query with *worst-case* O(1) space, and no amortization argument needed. Trade-off: the deque is exact-space for sparse traffic and makes `getHits` O(1); buckets are fixed-space and shine when hits vastly outnumber seconds.

## 5. Annotated Python solution

```python
from collections import deque


class HitCounter:
    def __init__(self):
        self.events = deque()   # (timestamp, count), timestamps strictly increasing
        self.total = 0          # hits currently inside the window

    def _evict(self, timestamp: int) -> None:
        # stale entries form a prefix; each entry is popped at most once ever
        while self.events and self.events[0][0] <= timestamp - 300:
            _, cnt = self.events.popleft()
            self.total -= cnt

    def hit(self, timestamp: int) -> None:
        if self.events and self.events[-1][0] == timestamp:
            ts, cnt = self.events[-1]
            self.events[-1] = (ts, cnt + 1)      # compress same-second hits
        else:
            self.events.append((timestamp, 1))
        self.total += 1
        self._evict(timestamp)

    def getHits(self, timestamp: int) -> int:
        self._evict(timestamp)                   # queries also advance time
        return self.total
```

The bucketed O(1)-space version:

```python
class HitCounter:
    def __init__(self):
        self.times = [0] * 300    # last timestamp that wrote each slot
        self.counts = [0] * 300

    def hit(self, timestamp: int) -> None:
        i = timestamp % 300
        if self.times[i] != timestamp:   # slot held a second >= 300s older
            self.times[i] = timestamp
            self.counts[i] = 0           # lazy reset: only when reclaimed
        self.counts[i] += 1

    def getHits(self, timestamp: int) -> int:
        return sum(c for t, c in zip(self.times, self.counts)
                   if t > timestamp - 300)
```

## 6. Complexity

- **Deque: amortized O(1)** per call — "every hit is pushed once and popped at most once, so total eviction work is bounded by total hits"; space O(min(window seconds, 300)) entries.
- **Buckets: O(1) hit, O(300) = O(1) getHits, worst-case O(1) space** — "the window is a fixed 300 seconds, so 300 slots cover it regardless of traffic."

## 7. Edge-case traps

- **The window boundary**: `getHits(301)` must drop a hit at 1 — the predicate is `ts > t - 300`, so eviction uses `<=`. Off-by-one here is *the* bug this problem exists to catch.
- **Duplicate timestamps** — three `hit(1)` calls are three hits; naive `(ts -> seen)` sets undercount.
- **`getHits` before any hit**, and after a gap so large the window is empty — must return 0, not crash on an empty deque.
- **`getHits` must also evict** (or at least filter): time advances on queries too, not only on hits.
- **Bucket lazy reset** — forgetting to zero a reclaimed slot silently adds 300-second-old traffic to new counts.

## 8. (DP section — not applicable)

Not DP. The reusable template: **evict-stale-prefix time window** — deque when you need exact per-event state, circular buckets when a fixed horizon lets you cap space; the same pair of idioms drives rate limiters and metrics rollups.

## 9. Interviewer follow-up

- *"Timestamps no longer arrive in order?"* — the prefix property dies. Buckets survive mild disorder (each slot keys on its own timestamp); for arbitrary disorder you need a sorted structure (`SortedList` / BST) with O(log n) inserts and range counts.
- *"Concurrent hits from many machines?"* — the deque's push/evict/total triple is a multi-word critical section (lock or single writer thread); the bucket array does better — per-slot atomics — but `getHits` then reads a torn snapshot, which is usually acceptable for metrics. Distributed version: each node keeps local buckets, the aggregator sums them — this is how real per-second metrics pipelines shard.
- *"Hits in the last hour, minute-granularity is fine?"* — 60 one-minute buckets: same structure, coarser slots; precision traded for space is a knob, and saying so is the mature answer.
- *"Not a counter but a rate limiter?"* — flip the question to per-key decisions and you get Logger Rate Limiter 359 territory: keep the newest allowed timestamp per key instead of every event.
