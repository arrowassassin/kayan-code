# Employee Free Time — Editorial

## 1. Pattern recognition

Strip the story: "when is nobody busy?" is the **complement of the union** of all intervals. The employee grouping is a distraction for correctness — a moment is shared free time iff it's covered by no interval at all — but it's a gift for efficiency, because each employee's list arrives **pre-sorted**, which invites a k-way heap merge instead of a global re-sort. This is the capstone of the Intervals chain: Merge Intervals builds the union, Insert Interval taught you to exploit given sortedness, and this problem asks for both plus a flipped output (the gaps, not the blocks).

## 2. Brute force first

Discretize: mark every unit of every interval busy in a timeline array, then read off unmarked runs — O(total interval length + T), up to ~10⁵ here so it'd actually survive, but it breaks the moment coordinates are floats or 10⁹, and interviewers will push exactly there. The honest baseline is flatten-everything + sort + merge: O(N log N) for N total intervals, ignoring the per-employee sortedness. That passes; the discussion point is whether you can do better *because* the lists are sorted — and saying "a min-heap gives O(N log k)" is the differentiator this Hard is really testing.

## 3. The key insight

**Merge all intervals (ignoring owners) into a single sorted busy timeline, and emit an interval exactly where consecutive busy blocks leave a positive gap.**

## 4. Step-by-step derivation

1. Reduce: common free time = complement of `union(all intervals)`, restricted to finite gaps. So compute the union as sorted disjoint blocks — the Merge Intervals scan verbatim.
2. That scan needs intervals sorted by **start** (merging = building unions ⇒ sort by start; contrast with sort-by-end, which serves *selection* problems — say this out loud when you choose). Route A: flatten and sort, O(N log N).
3. Route B: we're merging k already-sorted lists — the classic k-way merge. Min-heap holds one cursor per employee, keyed on the next interval's start; popping yields all N intervals in globally sorted start order at O(log k) per pop. Same scan downstream, O(N log k). This mirrors Merge k Sorted Lists, and naming that transfer is worth points.
4. Flip the output: keep `busy_until`, the right edge of the current merged block. For the next interval `[s, e]`: if `s <= busy_until`, extend with `max`; else `[busy_until, s]` is a window in which *no* interval is active — nobody is working — append it and start a new block at `[s, e]`.
5. Endpoint convention, stated explicitly: touching blocks (`[1,3]` then `[3,5]`) produce a zero-length "gap", which doesn't count — the `<=` in the extend test swallows it. Also drop the two infinite ends: emitting only *between* blocks does that for free.
6. Correctness of the gap claim: within a merged block someone is always working (that's what merging preserves); between blocks, by construction, every interval has ended and the next hasn't started.

## 5. Annotated Python solution

```python
import heapq


class Solution:
    def employeeFreeTime(self, schedule: list[list[list[int]]]) -> list[list[int]]:
        # k-way merge: one cursor per employee, keyed on next start.
        heap = [(emp[0][0], i, 0) for i, emp in enumerate(schedule)]
        heapq.heapify(heap)

        free = []
        busy_until = None                  # right edge of current merged busy block
        while heap:
            start, i, j = heapq.heappop(heap)   # globally smallest remaining start
            end = schedule[i][j][1]
            if busy_until is None or start <= busy_until:
                # <= : touching blocks leave no usable gap
                busy_until = end if busy_until is None else max(busy_until, end)
            else:
                free.append([busy_until, start])    # positive gap -> everyone idle
                busy_until = end
            if j + 1 < len(schedule[i]):            # advance this employee's cursor
                heapq.heappush(heap, (schedule[i][j + 1][0], i, j + 1))
        return free
```

The flatten-and-sort route is the same scan after `all_iv = sorted(iv for emp in schedule for iv in emp)` — fine to lead with, then offer the heap as the refinement.

## 6. Complexity

(N = total intervals, k = employees)

- **Time O(N log k)** heap route — "every interval enters and leaves the heap once, and the heap never holds more than one cursor per employee." (Flatten-and-sort: O(N log N).)
- **Space O(k)** for the heap plus the output — "one pending interval per employee."

## 7. Edge-case traps

- **Touching blocks across employees** (`[[1,3]], [[3,5]]`) → no gap; a `<` in the extend test invents a phantom `[3,3]`.
- **The infinite ends** — before the first meeting and after the last everyone is free, but those windows are unbounded and must not appear.
- **Nested intervals from different employees** (`[[1,10]], [[2,3]], [[4,5]]`) → the `max` extend keeps `busy_until` at 10; naive `busy_until = end` emits fake gaps inside `[1,10]`.
- **One employee** — the answer is just the spaces inside their own calendar; the pipeline shouldn't special-case it.
- **One interval total** → `[]`.
- **Interleaved fine-grained calendars** (the stress test: 10 employees × 2000 slivers) — exercises cursor advancement and mass gap emission.

## 8. (DP section — not applicable)

Not DP. This trains the **union-then-complement** move on top of the sort-by-start merge template, plus the **k-way heap merge** — the same trio behind Merge k Sorted Lists and calendar/availability systems.

## 9. Interviewer follow-up

- *"Only return gaps where at least `m` of the `k` employees are free"* — union/complement no longer suffices; switch to the +1/−1 **sweep line** (Meeting Rooms II's idiom) and emit stretches where the running busy-count `<= k - m`.
- *"Streaming calendars / can't fit in memory"* — the heap route already reads each list in order; it's naturally external — only k cursors live in RAM.
- *"Find the earliest common free slot of length ≥ d"* — same scan, return the first gap with `start - busy_until >= d`; this is the real-life "schedule a meeting" API.
- *"Timestamps are 64-bit epoch millis"* — nothing changes for the merge; it's the discretized-timeline brute force that dies, which is why you led with the sort/heap approach.
