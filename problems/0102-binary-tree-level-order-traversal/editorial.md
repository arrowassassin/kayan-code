# Binary Tree Level Order Traversal — Editorial

## 1. Pattern recognition

The output is grouped by **distance from the root** — and "process by distance" is the one thing BFS gives you that DFS doesn't. Any statement asking for levels, level sums, per-level maxima, the leftmost/rightmost node per level, or "minimum depth" should trigger the same reflex: breadth-first with a queue. This problem *is* the BFS level template in its purest form; nearly every other tree-BFS question (Zigzag 103, Right Side View 199) is this code plus a three-line twist, which is why it's worth over-learning.

## 2. Brute force first

The workable-but-clumsy route: compute the tree height, then for each depth `d` run a separate DFS that collects nodes at exactly depth `d`. That's O(n · h) — up to O(n²) ≈ 10^8 node visits on a skewed 10^4-node chain, which is exactly what the hidden stress test punishes. It also signals you don't know the level template. Every node only needs to be seen once; one traversal must suffice.

## 3. The key insight

**At the start of each round, the queue contains exactly one full level — so freezing `len(queue)` and popping precisely that many nodes peels off levels one at a time.**

## 4. Step-by-step derivation

1. Plain BFS visits nodes in level order but interleaves levels inside the queue: after popping the root you push its children, and the queue mixes "current" and "next" nodes as you continue.
2. The fix is an invariant, not extra bookkeeping: *if* the queue holds exactly level `d` when a round starts, and during the round you pop only those nodes (pushing their children), then when the round ends the queue holds exactly level `d+1`. Induction from the root does the rest.
3. So the template is: `while queue:` → `width = len(queue)` (snapshot **before** popping — the length changes as you push children) → pop `width` nodes into `level`, pushing non-null children → append `level`.
4. Use `collections.deque`: `list.pop(0)` is O(n) per pop and quietly turns the whole thing quadratic — same asymptotic sin as the brute force.
5. The recursive alternative — preorder DFS carrying `depth`, appending to `res[depth]`, creating the list on first visit — is equally correct and shorter. Trade-off to say out loud: DFS recursion is bounded by tree height, and a 10^4-node chain overflows CPython's default ~1000-frame limit unless you raise it; the iterative BFS has no such cliff. When the structure is "per level", BFS states your intent; when it's "per subtree", recursion does.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def levelOrder(self, root) -> list[list[int]]:
        if not root:
            return []
        res = []
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):  # snapshot: exactly one level
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(level)
        return res
```

## 6. Complexity

- **Time O(n)** — "every node is enqueued and dequeued exactly once; all queue operations are O(1) on a deque."
- **Space O(w)** for the queue, where `w` is the maximum level width (up to n/2) — "the queue never holds more than two adjacent levels' worth of nodes."

## 7. Edge-case traps

- **Empty tree** → `[]`, not `[[]]` — guard before creating the queue.
- **Skewed chain** → 10^4 levels of one node; this is where `list.pop(0)` or the per-depth re-DFS blows the time limit, and where a recursive DFS variant hits the default recursion limit.
- **Snapshotting `len(queue)` after pushing children** — the classic off-by-a-level bug; the length must be frozen before the inner loop.
- **Pushing null children** — either filter at push time (as above) or at pop time, but not neither and not both.

## 8. (DP section — not applicable)

Not DP. This *is* the reusable template — the BFS level loop (`width = len(queue)`, pop exactly `width`) — that Zigzag 103, Right Side View 199, and every "per-level statistic" problem are built on.

## 9. Interviewer follow-up

- *"Alternate the direction per level"* — Zigzag Level Order 103, the linked extension: identical loop, reverse every other `level` before appending.
- *"Bottom-up level order"* — same loop, `res.reverse()` at the end (or appendleft to a deque of levels).
- *"Average / max of each level, or rightmost node per level"* — replace `level.append` with an accumulator; rightmost-per-level is Right Side View 199.
- *"What if nodes had parent pointers and you got a list of nodes instead of a root?"* — level = distance from root; either walk up to compute depths or BFS from the root anyway; shows you understand level = BFS layer, not a stored attribute.

