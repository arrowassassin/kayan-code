# Vertical Order Traversal of a Binary Tree — Editorial

## 1. Pattern recognition

The give-away is that the statement assigns every node an explicit `(row, col)` **coordinate** before asking for any output. Whenever a tree question defines output order by geometry rather than by traversal (vertical order, top view, bottom view, diagonal view), the winning move is to *stop treating it as a traversal problem*: walk the tree once to tag nodes with coordinates, then let sorting/grouping arrange the tags. This is the coordinate generalization of Right Side View 199 (this problem's warmup): there, depth alone identified visibility; here, visibility-style questions need the second axis. The traversal and the ordering decouple completely — which is also why the intricate tie-break rule costs three lines instead of an algorithm redesign.

## 2. Brute force first

A traversal-centric attempt: find the column range `[min_col, max_col]`, then for each column run a full DFS collecting that column's nodes. O(n · width) — with width up to 2·10^4 on skewed trees, that's ~10^8 visits against the hidden 10^4-node chain (whose width *is* n). It also still needs the tie-break logic, so the complexity buys nothing. The one-pass collect-then-sort does strictly less work: every node is read once, then sorted once.

## 3. The key insight

**Tag every node with `(col, row, val)` in one DFS, then sort each column's `(row, val)` pairs — Python's tuple ordering is exactly the spec's ordering rule.**

## 4. Step-by-step derivation

1. Pass coordinates *down* the recursion: `dfs(node, row, col)` recurses into `(row+1, col-1)` and `(row+1, col+1)`. Nothing returns up — this is the pass-state-down half of tree recursion, with the accumulator being a `dict: col → list of (row, val)`.
2. Grouping by column first (a dict keyed by `col`) avoids one global sort of triples and makes the output shape direct: iterate `sorted(cols)`, emit each column's values.
3. Within a column the spec says: row ascending, then value ascending *only for identical `(row, col)`*. Sorting the `(row, val)` pairs lexicographically implements precisely that — value only ever breaks ties between equal rows, which is exactly the collision case. No special-case code for the tie rule at all; getting this without a same-cell flag is the whole trick of the problem.
4. Verify the subtle non-requirement: nodes in the same column but different rows must **not** be value-sorted — tuple order already leaves them in row order regardless of value. Visible example 2 (`5` before `6` at cell `(2,0)`, but `1` first despite being larger than nothing) is designed to check both directions.
5. DFS vs BFS trade-off: BFS visits rows in order, so each column's list comes out row-sorted and only same-cell runs need value-sorting — slightly less sorting, no recursion-depth worries on the 10^4 chain. The DFS form is shorter and relies on the judge's raised recursion limit; in stock CPython (default ~1000 frames) you'd raise it or go BFS. Saying that unprompted is the senior move.
6. Complexity of the sort phase: every node is sorted exactly once within its column, so the total is O(n log n) worst case (one giant column); the DFS itself is O(n).

## 5. Annotated Python solution

```python
from collections import defaultdict


class Solution:
    def verticalTraversal(self, root) -> list[list[int]]:
        cols = defaultdict(list)          # col -> [(row, val), ...]

        def dfs(node, row, col):
            if not node:
                return
            cols[col].append((row, node.val))
            dfs(node.left, row + 1, col - 1)
            dfs(node.right, row + 1, col + 1)

        dfs(root, 0, 0)
        # tuple sort = row asc, then val asc — val only decides same-cell ties
        return [[val for _, val in sorted(cols[c])] for c in sorted(cols)]
```

## 6. Complexity

- **Time O(n log n)** — "one O(n) walk, then each node participates in exactly one column sort; worst case all n share a column."
- **Space O(n)** — "the coordinate map stores one (row, val) pair per node, plus O(h) recursion."

## 7. Edge-case traps

- **Same-cell collisions** — `[1,2,3,4,6,5,7]`: `5` must precede `6`; missing the value tie-break passes most random tests and fails here.
- **Value-sorting a whole column** — the inverse bug: `[0,8,1,null,null,3,2,null,4,5,null]` has column entries whose row order disagrees with value order; sorting by `(val, row)` or plain `val` breaks it.
- **Skewed chains** — columns from `-(n-1)` to `n-1`; per-column re-DFS becomes quadratic, and DFS recursion depth hits 10^4.
- **Empty tree / single node** → `[]` / `[[1]]`.
- **Assuming column 0 is first** — the leftmost column can be far negative; iterate `sorted(cols)`, never `range(0, ...)`.

## 8. (DP section — not applicable)

Not DP. Template trained: **coordinate tagging + sort-by-tuple** — decouple the tree walk from the output geometry; the same recipe answers top view (keep the min-row entry per column), bottom view, and diagonal traversals.

## 9. Interviewer follow-up

- *"Top view / bottom view?"* — same tagging; per column keep only the smallest-row (or largest-row) entry, with a stated rule for same-cell ties.
- *"Why did LeetCode's older Vertical Order 314 give a different answer for collisions?"* — 314 orders same-cell nodes left-to-right by traversal instead of by value; implementation-wise the value sort becomes "stable BFS order", i.e. drop the tie-break and BFS. Knowing the spec difference is the point.
- *"Millions of nodes, tree on disk?"* — emit `(col, row, val)` records during a streaming walk and external-sort them; the decoupling means the algorithm survives the change of medium unchanged.
- *"Return columns as a dict keyed by column index?"* — trivially the intermediate structure; a reminder that the sorted-list output is presentation, not algorithm.
