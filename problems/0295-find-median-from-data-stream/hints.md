## Hint 1

Keeping a sorted list works (`bisect.insort`), but each insert shifts O(n) elements. Notice that `findMedian` never needs the whole ordering — only the one or two values sitting at the boundary between the smaller half and the larger half of the stream.

## Hint 2

Split the numbers into two halves: `lo` = the smaller half, `hi` = the larger half, with sizes differing by at most one. The median is determined entirely by the *maximum* of `lo` and the *minimum* of `hi`. Which structures give O(1) access to a max, and O(1) access to a min, with O(log n) inserts?

## Hint 3

A **max-heap** for `lo` and a **min-heap** for `hi` (in Python: one heap of negated values, one normal). On each `addNum`, push into `lo`, move `lo`'s max over to `hi` to restore ordering, then move one back if `hi` got bigger than `lo`. Two invariants — every `lo` value ≤ every `hi` value, and `len(lo) - len(hi) ∈ {0, 1}` — make `findMedian` a two-root read.
