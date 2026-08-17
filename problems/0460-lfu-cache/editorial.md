# LFU Cache — Editorial

## 1. Pattern recognition

"Design a class", "O(1) per operation", eviction by a *ranked* criterion with a tie-break — this is the escalation chapter of LRU Cache (146). LRU needed one ordering (recency); LFU needs a two-level ordering (frequency, then recency within a frequency). The design pattern is the same **composite data structure** fusion, applied one level deeper: when a single ordered structure can't encode your eviction rule, shard it into buckets and keep a pointer to the bucket you evict from. Snowflake's stream-processing design questions live exactly here: strict per-op budgets on stateful classes.

## 2. Brute force first

Keep `vals`, a `freq` counter dict, and a `last_used` timestamp dict. On eviction, scan all keys for the minimum `(freq, last_used)` pair — O(n) per eviction, O(n·q) overall. With 2×10⁵ operations over 10⁴ keys that's up to ~2×10⁹ comparisons: hopeless, and it violates the *stated* O(1) requirement anyway. A heap keyed on `(freq, last_used)` looks tempting but frequencies change on every access, forcing lazy deletion and O(log n) pushes — better, still not O(1).

## 3. The key insight

**Shard the cache by use counter — one recency-ordered bucket per frequency — and eviction is always "pop the oldest key from the bucket at `min_freq`", a pointer you can maintain in O(1) because frequencies only ever step up by exactly 1.**

## 4. Step-by-step derivation

1. Start from LRU: map + one recency list handles "evict the stalest". Here that list only resolves *ties*; the primary sort key is the counter. So keep **one recency structure per counter value**: `buckets[f]` = keys with counter `f`, oldest first. Notice: **LRU is just the special case where every key sits in the `f == 1` bucket forever.**
2. A touched key moves from bucket `f` to bucket `f + 1` and becomes the *newest* entry there — frequencies never jump, never decrease. That ±1 discipline is what makes the next step legal.
3. Eviction needs the smallest occupied frequency. Maintain `min_freq`: a fresh insert has counter 1 ≤ everything, so **every new insert sets `min_freq = 1`**; and if a touch drains the bucket at `min_freq`, its key went to `min_freq + 1`, so bump the pointer by one. No other event can lower or raise it — no scanning, ever.
4. Each bucket needs O(1) "remove this specific key" and O(1) "pop oldest". That's the LRU node-list role; in Python an `OrderedDict` (a hash map fused with a doubly linked list — literally LRU's structure, packaged) does both via `del d[k]` and `popitem(last=False)`.
5. Every operation is a few dict lookups plus one bucket-to-bucket move → O(1).

## 5. Annotated Python solution

```python
from collections import defaultdict, OrderedDict


class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.vals = {}                          # key -> value
        self.freq = {}                          # key -> use counter
        self.buckets = defaultdict(OrderedDict) # counter -> keys, oldest first
        self.min_freq = 0

    def _touch(self, key):                      # move key from bucket f to f+1
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:              # drained the minimum bucket:
                self.min_freq = f + 1           # its key moved exactly one up
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None         # appended -> newest in bucket

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)                        # a hit MUST bump the counter
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:                       # degenerate cache stores nothing
            return
        if key in self.vals:                    # update path: never evicts
            self.vals[key] = value
            self._touch(key)                    # updates count as uses too
            return
        if len(self.vals) == self.cap:          # evict BEFORE inserting
            victim, _ = self.buckets[self.min_freq].popitem(last=False)  # oldest = LRU tie-break
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[victim]
            del self.freq[victim]
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1                       # a counter-1 key is the new minimum
```

## 6. Complexity

- **Time O(1)** per `get`/`put` — "a constant number of dict operations plus one move between adjacent frequency buckets; `min_freq` updates by simple assignment, never by search."
- **Space O(capacity)** — "one value, one counter, and one bucket slot per cached key; empty buckets are deleted."

## 7. Edge-case traps

- **`capacity = 0`** — unlike LRU (146), the constraints allow it; `put` must be a no-op or eviction pops from an empty bucket and crashes.
- **`put` on an existing key at full capacity** must *not* evict — it's an update, size doesn't grow. Same classic bug as LRU, still the #1 killer here.
- **Updates must bump the counter**, not just replace the value — `put(k, v)` on a present key is a use.
- **Tie-break is recency**: two keys at the same counter evict oldest-touched first. Appending on touch and popping `last=False` encodes it; get the end wrong and every tie evicts backwards.
- **Forgetting `min_freq = 1` on insert** — after a run of hot keys, `min_freq` may be large; the next insert must drag it back down or the wrong bucket gets evicted.
- **Bumping `min_freq` only when the drained bucket *was* the minimum** — draining a higher bucket must leave the pointer alone.

## 8. (DP section — not applicable)

Not DP. The reusable skill: frequency-bucketed ordered structures plus a monotone minimum pointer — the same sharding rescues any "O(1) with a two-level eviction rule" design, and each bucket is a miniature LRU (146).

## 9. Interviewer follow-up

- *"Why does the `min_freq` pointer never need a search?"* — a favorite probe: counters only move by +1, and only the touched key moves, so the minimum either resets to 1 (insert) or follows its bucket up by one (drain). Being able to argue this invariant out loud is the difference between memorized and understood.
- *"Do it without `OrderedDict`"* — hand-roll each bucket as a sentinel-guarded doubly linked list with a shared `key -> node` map, exactly the LRU internals; buckets themselves can chain into a list of lists for the fully raw version.
- *"Aging / LFU with decay"* — pure LFU lets a key that was hot long ago squat forever on its stale high count; discuss halving counters periodically or the TinyLFU sketch-based admission filter used by real caches (Caffeine).
- *"Thread safety"* — one lock per operation is the honest answer; the buckets and `min_freq` form one invariant and cannot be locked piecemeal.
