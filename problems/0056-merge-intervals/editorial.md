# Merge Intervals — Editorial

## 1. Pattern recognition

The words "combine overlapping intervals" name the foundational Intervals pattern outright. The load-bearing detail is what the statement does **not** promise: the input is unsorted. That single fact dictates the whole plan — almost every interval problem becomes a linear scan *after* you impose an order, so the first decision to say out loud is "I'll sort, and here's the key I'll sort by." This is the warmup for the whole intervals chain (Insert Interval, Employee Free Time), and interviewers use it to check whether you can justify a sort key rather than recite one.

## 2. Brute force first

Without an order, treat merging as reachability: repeatedly scan all pairs, and whenever two intervals overlap, replace them with their union; stop when a full pass makes no change. Each pass is O(n²) and a chain like `[2,3],[4,5],...,[1,10]` can force many passes — O(n³) worst case. At n = 10⁴ that's ~10¹² operations, hopeless. The brute force's real lesson is *why* it's slow: overlap partners can be anywhere in the array, so you pay a search for every merge. Sorting exists precisely to make partners adjacent.

## 3. The key insight

**Once intervals are sorted by start, every merged group is a contiguous run, so a single left-to-right scan with one "current interval" being extended is enough.**

## 4. Step-by-step derivation

1. Why sort by **start** and not by end? Because the invariant we want during the scan is "everything that could extend the current group has not been seen yet." With starts increasing, when interval `i` arrives, every future interval starts at or after `intervals[i][0]` — so if `i` doesn't reach the current group, no later interval can sneak underneath and connect to it. Sorting by end gives no such guarantee for merging (it's the right key for the *selection* problems, like Non-overlapping Intervals — worth contrasting aloud).
2. Scan with a running interval `merged[-1]`. New interval `[s, e]`: if `s <= merged[-1][1]`, it overlaps or touches the running interval, so extend: `merged[-1][1] = max(merged[-1][1], e)`.
3. The `max` matters: a nested interval like `[2,3]` inside `[1,4]` must not drag the end backwards.
4. The `<=` encodes this problem's endpoint convention: **touching counts as overlapping** (`[1,4]` + `[4,5]` → `[1,5]`). State that convention explicitly before coding — it is a classic clarify-gate question, and other problems in this topic (Non-overlapping Intervals, Meeting Rooms II) deliberately choose the *opposite* convention.
5. If `s > merged[-1][1]`, the group is sealed forever (point 1 guarantees it); append `[s, e]` as a fresh group.

## 5. Annotated Python solution

```python
class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        # Sort by START: makes each merged group a contiguous run.
        intervals.sort(key=lambda it: it[0])

        merged = [intervals[0][:]]          # copy: don't alias the input row
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:      # <= : touching endpoints merge too
                # extend, never shrink — handles nested intervals
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])  # gap -> previous group is final
        return merged
```

## 6. Complexity

- **Time O(n log n)** — "the sort dominates; the merge scan itself is one O(n) pass."
- **Space O(n)** for the output — "O(1) auxiliary beyond the result (ignoring sort's internals)."

## 7. Edge-case traps

- **Touching endpoints** `[1,4],[4,5]` — must merge here; using `<` instead of `<=` silently splits them.
- **Nested interval** `[1,4],[2,3]` — writing `merged[-1][1] = end` instead of `max(...)` shrinks the group.
- **Single interval** — the scan body never runs; the seed must still come out.
- **Duplicates** `[0,5]×3` — collapse to one.
- **Reverse-sorted input** — catches anyone who quietly assumed sortedness (the exact assumption the follow-up, Insert Interval, *does* grant you).
- **Degenerate points** `[4,4],[4,4],[2,2]` — equal starts and zero width must still merge with each other, not crash the comparison.

## 8. (DP section — not applicable)

Not DP. This trains the reusable **sort-by-start + running-interval merge** template — the backbone that Insert Interval specializes and Employee Free Time inverts (emitting the gaps instead of the unions).

## 9. Interviewer follow-up

- *"The list is already sorted and disjoint; now insert one interval"* — that is Insert Interval 57, the linked follow-up: skip the sort and do a three-zone linear pass in O(n).
- *"Return the gaps instead of the merged blocks"* — same scan; whenever `s > merged[-1][1]`, emit `[current_end, s]` before starting the new group. Scaling that to many sorted schedules is Employee Free Time 759.
- *"Intervals arrive as a stream"* — you can't sort up front; keep merged intervals in an ordered structure and binary-search the overlap run per insert (Insert Interval repeated, ~O(log n) locate per operation).
- *"What if touching intervals should stay separate?"* — flip the one `<=` to `<`; being able to point at the exact character shows you own the convention.
