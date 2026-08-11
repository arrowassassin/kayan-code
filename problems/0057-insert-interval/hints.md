## Hint 1

The input is already sorted and non-overlapping — that's a gift. You never need to sort. Think about which existing intervals can possibly be affected by the new one.

## Hint 2

Partition the existing intervals into three zones: entirely **before** the new interval (`end < newStart`), **overlapping** it, and entirely **after** (`start > newEnd`). Only the middle zone changes.

## Hint 3

Walk left to right in one pass: copy the "before" zone untouched; while intervals overlap `[start, end]`, fold them in with `start = min(...)`, `end = max(...)`; emit the merged interval once; copy the rest. Watch the comparison operators — touching endpoints must merge.
