# Binary Tree Right Side View — Editorial

## 1. Pattern recognition

"What you see from the side" translates to **one representative per depth** — and grouping by depth is BFS territory. The problem is Level Order Traversal 102 with a projection applied: instead of keeping each level, keep its last element. Statements that reduce to "per-level min / max / first / last / sum" should all route to the same level template. The trap baked into the statement is the greedy misreading — "just follow right children" — which the constraints section openly warns about: the visible node can live in the left subtree when the right side is shallower.

## 2. Brute force first

Following `node.right` from the root gives a wrong answer, not a slow one (`[1,2,3,null,5]` breaks it) — so the real naive-but-correct baseline is: for each depth `d` from 0 to height, DFS to find the rightmost node at depth `d`. That's O(n·h): on the 10^4-node skewed chain in the hidden suite, ~5·10^7 visits and repeated work everywhere. One traversal already sees every node; extracting one value per level during that single pass must be possible.

## 3. The key insight

**During the standard BFS level loop, the last node popped in each round is exactly the one visible from the right.**

## 4. Step-by-step derivation

1. Run the 102 template: freeze `width = len(queue)` at the round start; the queue then holds one complete level, left to right.
2. Left-to-right order within the level is guaranteed because children are pushed left-then-right — so index `width - 1` is the rightmost node. Append only that value; children of *every* node in the level must still be pushed, or deeper levels lose nodes.
3. This drops the per-level list entirely — the projection happens inline, O(1) per level.
4. The elegant DFS alternative: visit **right child first**, carry `depth`, and append `node.val` when `depth == len(res)` (first arrival at a new depth is the rightmost node, because right-first order reaches each level's right end first). It's three lines — but it recurses to the tree's height, and a 10^4-node chain exceeds CPython's default ~1000-frame recursion limit; you'd raise the limit or convert to an explicit stack. The BFS version has no cliff. Naming that trade-off unprompted is worth more than either implementation.
5. Duality worth articulating: the DFS variant *returns nothing up and passes depth down* — it's the "pass constraints down" half of tree recursion, where `res` acts as shared state indexed by the passed-down depth.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def rightSideView(self, root) -> list[int]:
        if not root:
            return []
        res = []
        queue = deque([root])
        while queue:
            width = len(queue)
            for i in range(width):
                node = queue.popleft()
                if i == width - 1:   # last node of this level = visible one
                    res.append(node.val)
                if node.left:        # still expand EVERY node's children
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return res
```

## 6. Complexity

- **Time O(n)** — "one BFS; every node enters and leaves the queue exactly once."
- **Space O(w)**, `w` = maximum level width — "the queue is the only storage beyond the answer, and it never exceeds roughly one level."

## 7. Edge-case traps

- **Visible node in the left subtree** — `[1,2,3,null,5,null,4,6]`: depth 3's only node (6) hangs under the left side; right-chain walkers and any "stop when right is exhausted" logic fail here.
- **Left-skewed chain** — the entire view is the left spine; also the stress case that kills O(n·h) rescans and default-limit recursion.
- **Empty tree / single node** — `[]` and `[1]`; the empty guard must come before queue creation.
- **Forgetting to expand non-visible nodes' children** — output truncates below the first narrow level.

## 8. (DP section — not applicable)

Not DP. Template trained: the BFS level loop with an inline per-level projection — swap `i == width - 1` for `i == 0` (left view), `max` (per-level max), or `sum` (level averages) without touching the loop.

## 9. Interviewer follow-up

- *"Left side view?"* — keep index 0 instead of `width - 1`, or DFS left-first.
- *"Top view / bottom view?"* — depth alone no longer identifies visibility; you need horizontal coordinates per node — that's the coordinate framing of Vertical Order Traversal 987, this problem's linked extension.
- *"Return the nodes at the deepest level only?"* — same loop; keep the last `level` instead of one value per level.
- *"Stream the view while the tree mutates?"* — discuss recomputation vs. maintaining rightmost-per-depth in a map keyed by depth, updated on insert/delete.
