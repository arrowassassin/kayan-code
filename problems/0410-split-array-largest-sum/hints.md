## Hint 1

Flip the question around. Instead of "given k pieces, what's the best largest sum?", ask "given a cap on the largest sum, how few contiguous pieces do I need?" — one of these directions is much easier to compute than the other.

## Hint 2

For a candidate cap `limit`, a greedy pass answers it: extend the current block until adding the next element would push its sum past `limit`, then cut. If that minimal piece count is at most `k`, the cap is achievable — and any larger cap is too. Feasibility is monotonic in the cap.

## Hint 3

Binary search the cap between `max(nums)` (every element must fit in some block) and `sum(nums)` (one block). Smallest feasible cap = the answer. If the greedy needs `<= k` pieces you may pad with extra cuts to use exactly `k` (elements are non-negative), so "at most k" and "exactly k" coincide. This mirrors Ship Packages: capacity ↔ cap, days ↔ k.
