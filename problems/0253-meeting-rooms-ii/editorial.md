# Meeting Rooms II — Editorial

## 1. Pattern recognition

"Minimum number of rooms" is not a merge and not a subset selection — it's a **maximum concurrent overlap** question: the answer equals the largest number of meetings alive at any single instant. That reframing unlocks two canonical Intervals tools at once: the **min-heap of end times** (simulate room reuse) and the **sweep line** (+1/−1 event counting). Interviewers love this problem because it forces the sort-key discussion *and* has two clean solutions worth comparing aloud.

## 2. Brute force first

For every meeting, count how many other meetings overlap it, and take the max — O(n²). Or discretize time: increment a counter for every unit of every meeting — O(n · duration), up to 10⁵ × 10⁶ here. Both die at these constraints (10¹⁰-ish operations against a 3-second limit). The n = 10⁵ constraint again whispers "sort + linear/heap scan, O(n log n)."

## 3. The key insight

**Rooms only matter in aggregate: the minimum number of rooms equals the peak count of simultaneously running meetings, and that peak can be found by processing sorted start/end times in order.**

## 4. Step-by-step derivation

1. Lower bound: if `k` meetings overlap at one instant, you need ≥ `k` rooms. Achievability: a greedy that reuses the earliest-freeing room never opens a room unless forced, so it uses exactly the peak. Hence answer = peak concurrency.
2. **Heap simulation.** Sort meetings by **start** — we must seat meetings in the order they begin; sorting by end would seat a meeting before knowing what's already running. Maintain a min-heap of end times of occupied rooms. For meeting `[s, e]`: if the smallest end time `<= s`, that room is free — *replace* the top with `e` (reuse). Otherwise every room is still busy — push `e` (open a room). The heap's final size is the peak. Only the *earliest* end matters for the free-or-not test: if the earliest-freeing room isn't free, none are.
3. **Sweep line.** Decompose each meeting into two events: `(s, +1)` and `(e, -1)`. Sort all events by time and run a counter; the running maximum is the answer. This is the same idiom that solves "max concurrent users", "min platforms", "car pooling".
4. Endpoint convention, stated explicitly: slots are **half-open**, so `[1,5]` and `[5,10]` share a room. In the heap this is `ends[0] <= start` (not `<`); in the sweep it means departures sort **before** arrivals at equal timestamps — e.g. sort pairs `(time, delta)` with `-1 < +1`. Get the tie order backwards and you overcount by one. This is the clarify-gate question: always ask (or declare) whether a meeting ending at `t` frees the room for one starting at `t`.
5. Both are O(n log n); the heap variant also tells you *which* room frees when — handy for follow-ups that assign rooms.

## 5. Annotated Python solution

```python
import heapq


class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        # Sort by START: seat meetings in the order they begin.
        intervals.sort(key=lambda it: it[0])

        ends = []                          # min-heap: end times of occupied rooms
        for start, end in intervals:
            if ends and ends[0] <= start:  # <= : ending at t frees the room for t
                heapq.heapreplace(ends, end)   # reuse the earliest-freeing room
            else:
                heapq.heappush(ends, end)      # all rooms busy -> open a new one
        return len(ends)                   # heap size == peak concurrency
```

The sweep-line alternative, equally interview-ready:

```python
class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        events = []
        for s, e in intervals:
            events.append((s, 1))          # arrival
            events.append((e, -1))         # departure
        events.sort()                      # ties: (t,-1) before (t,+1) automatically

        rooms = peak = 0
        for _, delta in events:
            rooms += delta
            peak = max(peak, rooms)
        return peak
```

## 6. Complexity

- **Time O(n log n)** — "sorting dominates; each meeting costs one O(log n) heap operation (or two sorted events)."
- **Space O(n)** — "the heap can hold every meeting in the worst case (all overlapping); the sweep stores 2n events."

## 7. Edge-case traps

- **Back-to-back meetings** `[1,5],[5,10],[10,15]` → 1 room. `<` instead of `<=` (or arrivals sorted before departures in the sweep) answers 2.
- **Identical meetings** `[0,10]×3` → 3; the heap must push all three.
- **One meeting** → 1, never 0.
- **A later-starting meeting ending before an earlier one** (`[[13,15],[1,13]]`) — unsorted input punishes anyone who skipped the sort.
- **Forgetting `heapreplace` frees before it seats** — pushing without popping when a room is free inflates the heap and the answer.
- **Staircase overlap** (the stress test: 10⁵ meetings, each overlapping the next 9) — peak is 10; brute-force pairwise counting TLEs.

## 8. (DP section — not applicable)

Not DP. This trains two reusable templates at once: the **min-heap of end times** (resource reuse under start-order processing) and the **+1/−1 sweep-line counter** — the pair reappears in Car Pooling, Minimum Platforms, and Employee Free Time's merged-busy timeline.

## 9. Interviewer follow-up

- *"Also return which room each meeting uses"* — heap entries become `(end, room_id)`; on reuse, assign the popped room's id; new rooms get fresh ids. The sweep can't do this — a good reason to prefer the heap.
- *"Rooms have capacities / meetings have sizes"* — sweep still finds peak *load* if you use `+size/−size` deltas; assignment becomes bin-packing-ish and worth discussing, not solving.
- *"Given the rooms count k, can the schedule fit?"* — run the same peak computation and compare to k; streaming version keeps the heap online.
- *"What's the maximum number of meetings one room could host instead?"* — that flips you back to sort-by-end greedy selection (Non-overlapping Intervals 435, this problem's warmup).
