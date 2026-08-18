# Insert Interval — Editorial

## 1. Pattern recognition

The statement hands you **sorted, non-overlapping** intervals and asks you to keep that invariant after one change. Whenever an input arrives pre-sorted, the intended solution almost always exploits that order in a **single linear pass** — reaching for "sort then merge" (the generic Merge Intervals recipe) throws the gift away. This is a frequently-reported interview question, and the trap it sets is exactly that: candidates who memorized Merge Intervals re-sort an already-sorted input.

## 2. Brute force first

Append `newInterval`, sort everything, then run the standard merge scan: O(n log n) time. It *passes* — but it's the generic tool where a specialized O(n) exists, and an interviewer who chose *Insert* Interval over *Merge* Intervals wants to see you notice the difference. Saying "I could sort-and-merge in n log n, but the input's sortedness lets me do one linear pass" is the expected opening move.

## 3. The key insight

**Only a contiguous middle block of intervals can overlap the new one — everything before it and after it passes through untouched.**

## 4. Step-by-step derivation

1. Since intervals are sorted and disjoint, the ones overlapping `[s, e]` form one contiguous run. Intervals with `end < s` are entirely left of it; intervals with `start > e` entirely right.
2. So: **copy** the left zone verbatim (`intervals[i][1] < start`).
3. **Fold** the overlapping run into the new interval: while `intervals[i][0] <= end`, set `start = min(start, interval.start)`, `end = max(end, interval.end)`. The `<=`/`<` boundaries encode "touching counts as overlapping" — flip either one and adjacent intervals wrongly stay split.
4. **Emit** the folded interval exactly once, then copy the right zone verbatim.
5. Each interval is examined once → O(n).

## 5. Annotated Python solution

```python
class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        res = []
        i, n = 0, len(intervals)
        start, end = newInterval

        # 1) strictly before: ends before the new interval starts
        while i < n and intervals[i][1] < start:
            res.append(intervals[i])
            i += 1

        # 2) overlap zone: starts no later than our current end -> absorb.
        #    <= not <, so touching intervals merge.
        while i < n and intervals[i][0] <= end:
            start = min(start, intervals[i][0])
            end = max(end, intervals[i][1])
            i += 1
        res.append([start, end])

        # 3) strictly after
        res.extend(intervals[i:])
        return res
```

## 6. Complexity

- **Time O(n)** — "one pass; each interval is compared a constant number of times."
- **Space O(n)** for the output — "O(1) extra beyond the result list."

## 7. Edge-case traps

- **Empty `intervals`** → answer is just `[newInterval]`; the loops must fall through cleanly.
- **New interval before everything / after everything** — zone 2 absorbs nothing; make sure the emit still happens in the right position.
- **Touching endpoints** `[1,2] + [2,3]` → must merge; this is where `<` vs `<=` bites.
- **New interval swallowed whole** by an existing one (`[[1,10]]`, new `[4,5]`) — min/max handles it, but test it.
- **New interval spanning the entire list** — everything folds into one.

## 8. (DP section — not applicable)

Not DP. The reusable skill is the three-zone linear scan; it also powers Merge Intervals (this problem's warmup) and the sweep in Employee Free Time (its follow-up).

## 9. Interviewer follow-up

- *"Now do it for `k` schedules of intervals and find the free gaps"* — that is Employee Free Time 759, the linked extension: flatten + heap-merge the sorted lists, or sweep by start, tracking the running max end; gaps appear when `next.start > running_end`.
- *"What if inserts arrive repeatedly?"* — keep the list in a balanced structure; each insert is O(log n) to locate the overlap run via binary search (`bisect` on starts) plus the splice cost; mention an interval tree for heavy workloads.
- *"Return the number of merges instead"* — same scan, count zone-2 absorptions.
