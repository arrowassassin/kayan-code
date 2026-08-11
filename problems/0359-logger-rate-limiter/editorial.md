# Logger Rate Limiter — Editorial

## 1. Pattern recognition

"Stream of timestamped events, per-key throttling decision, O(1) per call" — this is the **keyed stream state** flavor of the stream-design family: instead of one shared window (Moving Average, Hit Counter), you keep one tiny piece of state *per message key*. The give-away in the statement is that different messages never interact — whenever keys are independent, the design collapses to "a dict from key to the minimal fact needed for the next decision". Stating the per-op budget up front — "each call must be one hash lookup" — is the expected opening.

## 2. Brute force first

Keep every `(timestamp, message)` ever accepted; on each call, scan for the most recent accepted occurrence of this message and compare. O(n) per call, O(n) memory, so 10⁴ calls cost up to ~10⁸ pair inspections — sluggish, but the deeper flaw is storing history when only the latest fact per key matters. A stream design is graded on what it *refuses* to remember.

## 3. The key insight

**Per message, the entire past compresses into one number — the earliest timestamp at which it may print again — and each call is one lookup plus one comparison against it.**

## 4. Step-by-step derivation

1. The decision for `message` at time `t` depends only on the last time it *printed* (not on rejected attempts — they don't reset the timer). So keep `next_ok[message] = last_print + 10`.
2. Storing `next_ok` rather than `last_print` moves the `+10` out of the hot comparison and makes the boundary explicit: allowed iff `t >= next_ok`, i.e. rejected iff `t < next_ok`. Arriving exactly 10 seconds later prints — `<`, not `<=`.
3. Update the entry **only on the True path**. Updating on rejection would let a chatty message starve itself forever — the classic bug here, and exactly what a hidden test targets.
4. Each call: one `dict.get`, one comparison, maybe one assignment → O(1) average per call.
5. Memory grows with the number of *distinct* messages, not with call count — fine for this problem's constraints, but it is the honest weakness the follow-up pokes at: entries for messages never seen again live forever. Cleanup options: (a) piggyback eviction — since timestamps are non-decreasing, keep keys in an auxiliary queue ordered by expiry and pop entries with `next_ok <= t` on each call (amortized O(1), the Hit Counter idiom reused); (b) bound the map with an LRU policy — which is literally LRU Cache 146.

## 5. Annotated Python solution

```python
class Logger:
    def __init__(self):
        self.next_ok = {}   # message -> earliest timestamp allowed to print

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if timestamp < self.next_ok.get(message, 0):
            return False            # rejected: do NOT touch the timer
        self.next_ok[message] = timestamp + 10   # printed: reset window
        return True
```

## 6. Complexity

- **Time O(1)** average per call — "one hash lookup, one comparison, at most one store; string hashing is O(length), and messages are capped at 30 chars."
- **Space O(k)** for k distinct messages — "one integer per key ever seen; note this never shrinks without explicit cleanup."

## 7. Edge-case traps

- **Rejected duplicates must not reset the timer** — update only when returning `True`.
- **Exact boundary**: printed at `t`, a duplicate at `t + 10` prints; `<=` in the guard gets this wrong.
- **Same timestamp, same message twice** — first `True`, second `False`; `timestamp = 0` must work (make the default sentinel 0, not `-1`-with-`<=`).
- **Different messages at the same timestamp** are all independent — no shared window.
- **Unbounded key growth** — not a correctness bug in tests, but the interviewer will ask; have the expiry-queue or LRU-bound answer ready.

## 8. (DP section — not applicable)

Not DP. The reusable template: **per-key latest-fact dict** — compress each key's history to the one value the next decision needs; the same shape answers de-dup, sessionization and token-bucket questions.

## 9. Interviewer follow-up

- *"Memory keeps growing — fix it"* — the intended extension. Any entry with `next_ok <= now` is dead weight; sweep with an expiry-ordered queue (amortized O(1) per call, works because timestamps are non-decreasing), or cap the dict with LRU eviction — correctness survives evicting live keys? No: an evicted live key would wrongly print, so an LRU bound trades exactness for bounded memory; say that trade out loud.
- *"At most k prints per 10 seconds instead of 1"* — one timestamp no longer suffices; keep a per-key deque of print times and evict stale ones — the Hit Counter window, now per key.
- *"Multiple logger instances behind a load balancer"* — per-node dicts drift; either hash-partition messages to nodes (each key has one owner) or centralize state in Redis with `SET key EX 10 NX`, which is this exact algorithm as one atomic command.
- *"Out-of-order timestamps?"* — the `<` test still works per call, but "printed at t blocks until t+10" becomes ambiguous when an earlier event arrives late; you must define whether the limiter is on event time or arrival time — a real streaming-systems conversation.
