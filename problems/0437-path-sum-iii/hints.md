## Hint 1

The obvious plan — start a fresh downward sum-count from every node — works but does O(n²) work on skewed trees. Notice what all paths ending at one node have in common: they are suffixes of the single root-to-node path.

## Hint 2

If `prefix[v]` is the sum from the root down to node `v`, then the path from `u`'s child down to `v` sums to `prefix[v] - prefix[u]`. So paths ending at `v` with the target sum correspond to ancestors `u` with `prefix[u] = prefix[v] - target`. How would you have those ancestor prefix sums available at `v` — this is the Two Sum / subarray-sum trick, transplanted onto a root path.

## Hint 3

DFS carrying the running sum, plus a hashmap `count[prefix_sum]` describing only the **current root-to-node path**. At each node: add `count[running - target]` to the answer, increment `count[running]`, recurse children, then decrement it on the way out — the undo is what stops one branch's prefixes from leaking into a sibling. Seed the map with `{0: 1}` for paths that start at the root.
