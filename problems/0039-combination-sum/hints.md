## Hint 1

This is Subsets with two twists: a partial selection is only recorded when its sum hits `target`, and an element may be picked again. Start from the same decision-tree recursion — a shared `path`, a `start` index — and ask what each twist changes.

## Hint 2

To allow reuse *without* producing both `[2,3,2]` and `[2,2,3]`, keep the "never look backwards" rule but soften it by one: when you choose `candidates[i]`, recurse with `start = i` (not `i + 1`). Each combination is then generated exactly once, in non-decreasing index order — no dedup set needed.

## Hint 3

Track `remaining = target - sum(path)` as a parameter instead of re-summing. Record `path[:]` when `remaining == 0`; abandon the branch when a candidate exceeds `remaining`. If you **sort** the candidates first, the moment one candidate is too big you can `break` out of the whole loop — every later candidate is bigger still. That sort-then-break prune is the difference between wandering the full tree and cutting dead branches at first contact.
