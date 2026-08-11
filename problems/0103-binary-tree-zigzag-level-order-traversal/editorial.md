# Binary Tree Zigzag Level Order Traversal — Editorial

## 1. Pattern recognition

"Level by level" → BFS level template, full stop. The zigzag wording is set dressing: the *contents* of every level are exactly those of Level Order Traversal 102 (this problem's warmup); only the reading direction of alternate levels flips. Recognizing that the delta from a known template is one boolean and one `reverse()` — and saying so within the first minute — is the entire test. Candidates get into trouble precisely when they take the zigzag too seriously and try to make the traversal itself snake.

## 2. Brute force first

The tempting "faithful" simulation: actually traverse right-to-left on odd levels, e.g. by reversing the queue each round, or pushing children in alternating order onto a stack pair. It's still O(n), so it doesn't TLE — it fails by *fragility*: reversing the live queue reorders which children are discovered next round, and the alternating push order has four cases that are easy to mis-mirror. When two designs have equal complexity, pick the one with fewer moving parts; here that's "traverse normally, flip the finished level".

## 3. The key insight

**Traversal order and presentation order are independent — collect every level left-to-right as usual, then reverse the finished list on alternate levels.**

## 4. Step-by-step derivation

1. Start from the 102 template: `while queue:` → freeze `width = len(queue)` → pop exactly `width` nodes, appending values to `level` and pushing non-null children left-then-right.
2. The invariant (queue holds exactly one complete level at each round start) is untouched by anything we do to `level` after the inner loop — that's why post-processing is safe and queue surgery is not.
3. Keep `left_to_right = True`; after each level, append `level` or `level[::-1]` and flip the flag. Reversal cost totals O(n) across all levels — asymptotically free.
4. If the interviewer wants "no reversal at all": keep `level` as a `deque` and `appendleft` on odd levels while still *popping* in normal order. Same idea — direction applied at insertion into the output, never to the traversal.
5. A DFS variant also exists (append to `res[depth]`, reverse odd rows at the end) — mention the trade-off: recursion depth equals tree height, so a 10^4-node chain needs a raised recursion limit in stock CPython, while the BFS loop is immune. For per-level output, BFS is the natural fit.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def zigzagLevelOrder(self, root) -> list[list[int]]:
        if not root:
            return []
        res = []
        queue = deque([root])
        left_to_right = True
        while queue:
            level = []
            for _ in range(len(queue)):   # snapshot: exactly one level
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            # presentation flip only; the queue is never touched
            res.append(level if left_to_right else level[::-1])
            left_to_right = not left_to_right
        return res
```

## 6. Complexity

- **Time O(n)** — "each node is enqueued and dequeued once; the alternate-level reversals sum to at most n element moves."
- **Space O(w)**, `w` = widest level — "the queue holds at most about one level, up to n/2 nodes on the last full level."

## 7. Edge-case traps

- **Empty tree** → `[]` before any queue exists.
- **Single-child chains** — every level has one node, so reversal is invisible; a bug that reverses the *wrong* levels can still pass these. The full-tree cases catch it: level 1 must be `[3,2]`, not `[2,3]`.
- **Flag flipped before appending** instead of after — shifts the zigzag by one level; the first level must always read left-to-right.
- **Reversing the queue instead of the level** — scrambles child discovery order on the following level; test `[1,2,3,null,4,5,null,6,null,null,7]` exists to expose exactly this.

## 8. (DP section — not applicable)

Not DP. Reusable template: the BFS level loop from 102 plus the "decorate the finished level, never the traversal" discipline — the same separation that makes bottom-up level order and per-level statistics one-line variants.

## 9. Interviewer follow-up

- *"Spiral order for an n-ary tree?"* — identical loop; push all children, flip the finished level.
- *"Zigzag but return a single flat list?"* — same code, `res.extend` instead of `res.append`.
- *"Constant extra output work — no reversals?"* — the `deque` + `appendleft` variant above; or track an index and fill a pre-sized list from either end.
- *"Column zigzag instead of row zigzag?"* — that's a vertical traversal with direction — see Vertical Order Traversal 987 for the coordinate-based framing.
