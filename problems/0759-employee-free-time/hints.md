## Hint 1

Employee boundaries are a red herring: a moment is shared free time exactly when it lies inside *nobody's* interval. So the problem is really about the union of all intervals, regardless of whose they are.

## Hint 2

If you had the merged busy timeline — the union as sorted, disjoint blocks — the answer is just the spaces between consecutive blocks. You already know how to build that union from Merge Intervals. What changes is what you *emit*.

## Hint 3

Two routes: (a) flatten all intervals into one list, sort by start, and run the merge scan, but record `[current_end, next_start]` whenever a real gap appears (`next_start > current_end`; touching means no gap). (b) Since each employee's list is already sorted, do a k-way merge with a min-heap keyed on start — same scan, no global sort. Drop the infinite stretches before the first block and after the last.
