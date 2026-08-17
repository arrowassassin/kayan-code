## Hint 1

Don't try to enumerate subsets "by size" or with clever index math first. Think about building one subset at a time through a sequence of decisions: what is the one yes/no question you can ask about each element?

## Hint 2

For each element, either it is in the current subset or it is not. That gives a binary decision tree of depth `n` with exactly `2^n` leaves — one per subset. A recursive function that carries the current partial subset (`path`) and the index of the next element to decide on visits all of them.

## Hint 3

Write `backtrack(start)`: record a copy of `path` (every node of the tree is itself a valid subset, not just the leaves), then for each `i` from `start` to the end — append `nums[i]`, recurse with `i + 1`, pop it back off. The pop is the "unchoose" step: without it, `path` carries stale elements into sibling branches. (There is also a neat non-recursive route: start from `[[]]` and, for each number, extend every subset built so far with it.)
