## Hint 1

A substring that is a rearrangement of `s1` must have the same length as `s1` — so you're not searching arbitrary windows, only windows of one **fixed size** sliding across `s2`. What property of a window makes it a permutation of `s1`?

## Hint 2

Two strings are permutations of each other iff their 26-letter count vectors are identical. Keep a count vector for `s1` and one for the current window of `s2`; when the window slides one step, exactly one letter enters and one leaves.

## Hint 3

Comparing two 26-length arrays at every slide is fine (O(26n)), but you can make each slide O(1): maintain `matches` = how many of the 26 letters currently agree between window and target, and adjust it only for the two letters whose counts changed. Return `True` the moment `matches == 26`; handle `len(s1) > len(s2)` up front.
