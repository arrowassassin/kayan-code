## Hint 1

Peel away the baskets story: "start somewhere, walk right, stop when a third type appears" is asking for the longest **contiguous subarray with at most 2 distinct values**. That phrasing should immediately suggest a sliding window.

## Hint 2

The window invariant is "at most 2 distinct types". Removing elements from the left can only reduce the number of distinct types, so the invariant is repairable by shrinking — the precondition for the standard template. What structure tells you the number of distinct types in the window in O(1)?

## Hint 3

Keep `count[type]` for the window. Expand `right` each step; while the map has 3 keys, decrement `count[fruits[left]]` and — crucially — **delete the key when its count hits 0**, then advance `left`. Track the max window length. If you forget the deletion, `len(count)` lies and the window shrinks forever.
