# Path Sum III — Editorial

## 1. Pattern recognition

"Count downward paths with a given sum, starting anywhere" is Subarray Sum Equals K 560 wearing a tree costume. The mapping: a downward path is a contiguous *segment* of some root-to-node path, exactly as a subarray is a contiguous segment of an array — and "count segments with sum k" has a canonical O(n) answer via **prefix sums + a hashmap**. The extra twist trees add: the "array" branches, so the hashmap must describe only the *current* root path, which forces backtracking. Negative values (called out in the constraints) are the same tell as in 560 — they rule out sliding-window or sum-based pruning. Where the warmup Diameter 543 returned a tiny summary up, this problem's state flows *down* the recursion; it's the other half of the duality.

## 2. Brute force first

Double DFS: for every node `u`, run a second DFS below `u` accumulating sums and counting hits. Correct and easy — and O(n²): each node is re-visited once per ancestor. On the hidden 10^4-node chain that's ~5·10^7 sum extensions plus interpreter overhead, which is exactly what the 3-second stress case is tuned to kill. The observation that rescues it: the inner DFS keeps recomputing sums of overlapping path segments, and *all* segments ending at a fixed node are suffixes of one root path — differences of two prefix sums.

## 3. The key insight

**A downward path `u→v` sums to `target` iff `prefix[v] − prefix[parent-of-u] = target` — so at each node, count ancestors whose prefix sum equals `running − target`, kept in a hashmap that is un-done when the DFS leaves the node.**

## 4. Step-by-step derivation

1. Define `prefix[v]` = sum of values from the root to `v` inclusive. Any downward path ending at `v` is `prefix[v] − prefix[u]` for the ancestor `u` just above the path's start.
2. So while standing at `v` with `running = prefix[v]`, the number of valid paths ending at `v` is the number of ancestors (including the "empty" ancestor above the root) with prefix sum `running − target`. A hashmap `seen: prefix → count` over the current path answers that in O(1).
3. Seed `seen = {0: 1}`: the empty prefix stands for paths that begin at the root itself. Forgetting it silently drops every root-starting path — the most common wrong-answer here.
4. Order of operations at a node matters when `target == 0`: query `seen[running − target]` **before** inserting `running`, or the node pairs with itself and `[0,0,0]`-style cases (in the hidden suite) overcount.
5. After recursing into both children, decrement `seen[running]`. The map must describe only the root-to-current path; without the undo, a left-subtree prefix can "complete" a path for a right-subtree node — cousins are not ancestors. This increment/recurse/decrement shape is textbook backtracking on shared state.
6. Duplicate prefix values happen (zeros, negatives), hence counts, not a set. Recursion depth = height = 10^4 on the chain test — over stock CPython's ~1000 default (fine under this judge's raised limit); the honest caveat is "raise the limit or convert to an explicit stack carrying (node, running, phase) so the decrement still fires."

## 5. Annotated Python solution

```python
from collections import defaultdict


class Solution:
    def pathSum(self, root, targetSum: int) -> int:
        seen = defaultdict(int)   # prefix sum -> count on CURRENT root path
        seen[0] = 1               # empty prefix: paths starting at the root
        self.count = 0

        def dfs(node, running):
            if not node:
                return
            running += node.val
            # query BEFORE insert: a node must not pair with itself
            self.count += seen[running - targetSum]
            seen[running] += 1
            dfs(node.left, running)
            dfs(node.right, running)
            seen[running] -= 1    # backtrack: leave no trace for siblings

        dfs(root, 0)
        return self.count
```

## 6. Complexity

- **Time O(n)** — "one DFS; each node does O(1) hashmap work."
- **Space O(h)** for the map and stack — "the map only ever holds the prefixes of one root-to-node path, at most h+1 entries."

## 7. Edge-case traps

- **`target = 0` with zero-valued nodes** — `[0,0,0]` → 5; query-before-insert and counting (not a set) are both load-bearing.
- **Negative values** — `[1,-2,-3,...], target −1`: running sums oscillate; any pruning on "sum too big" is wrong.
- **Missing `seen[0] = 1`** — every path anchored at the root vanishes; visible example 1 already catches it.
- **Missing decrement** — overcounts across sibling branches; shows up on bushy trees, not chains, which is why both shapes are tested.
- **Deep chain** — O(n²) brute force TLEs; recursion depth needs the raised limit.
- **Empty tree** → 0 without special-casing (the DFS just returns).

## 8. (DP section — not applicable)

Not DP. Template trained: **prefix-sum + hashmap transplanted onto the recursion path, with backtracking undo** — the tree version of Subarray Sum Equals K 560, and the general recipe for any "count segments of a root path" query.

## 9. Interviewer follow-up

- *"Return the paths themselves"* — carry the current path list; on a hit you'd need which ancestors matched, so store lists of depths (or prefix→depths) instead of bare counts, and slice the path.
- *"Longest path with sum k instead of the count"* — store the *shallowest depth* per prefix value instead of a count; maximize `depth(v) − depth(u)`.
- *"Paths may also go up and over (any simple path)?"* — this trick breaks; you're back to per-bend combination à la Diameter 543 / Max Path Sum 124, merging sum-multisets or using small-to-large tricks.
- *"Stream of updates to node values?"* — root-path prefix structure invalidates on update; discuss Euler tour + BIT over subtree ranges as the heavier machinery.
