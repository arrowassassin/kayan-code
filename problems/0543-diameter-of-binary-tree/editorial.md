# Diameter of Binary Tree — Editorial

## 1. Pattern recognition

"Longest path between any two nodes" with paths allowed to *bend* anywhere is the signature of the **combine-two-arms-at-every-node** family: Diameter, Binary Tree Maximum Path Sum 124, Longest Univalue Path 687 all share it. The tell in the statement is "may or may not pass through the root" — the answer is a property of *some* node's two subtrees, but you don't know which node, so every node must try being the bend point. That means a post-order DFS that returns a small summary (here: height) upward while a side channel tracks the best bend seen — the canonical "return info up" half of tree recursion.

## 2. Brute force first

For each node, compute the height of its left and right subtrees with a fresh recursive `height()` call, and take the max of `lh + rh + 2` over all nodes. Correct — and O(n) height computations of O(n) each = **O(n²)**. On the hidden 10^4-node chain that's ~5·10^7 redundant node visits plus deep recursion; it's precisely the case the stress test targets. The waste is obvious once said aloud: `height(node)` recomputes `height(child)` from scratch even though the child's answer was just computed one call earlier.

## 3. The key insight

**Height and diameter can be computed in the same post-order pass: return the height up, and update the best `left + right + 2` as a side effect at each node.**

## 4. Step-by-step derivation

1. Classify every path by its unique topmost node `b` (the bend). Below `b`, each side of the path is a straight downward chain, so its best possible length is the height of that subtree.
2. Longest path bending at `b` = `height(b.left) + height(b.right) + 2` (the two edges from `b` to its children). The diameter is the max of this over all `b`.
3. Brute force recomputes heights; but post-order already visits children before parents — so when the recursion returns from `b`'s children, both heights are in hand. Fold the diameter update into the height function: one pass, O(n).
4. Convention choice that removes all special cases: `height(None) = -1` (edges convention). Then a leaf has height `0` and `lh + rh + 2` correctly gives `0` for a leaf's bend. If you instead count nodes (`height(None) = 0`), the bend formula becomes `lh + rh` — either works, but mixing them is the classic off-by-one; declare your convention out loud before coding.
5. Recursion vs iteration: this is naturally recursive (post-order needs children first). Depth = tree height = up to 10^4 on the chain test — beyond CPython's default ~1000-frame limit, though comfortably inside this judge's raised limit. In production Python you'd say: raise the limit, or do an explicit-stack post-order. The BFS level template is no help here; "per-subtree" problems belong to DFS the way "per-level" ones belong to BFS.

## 5. Annotated Python solution

```python
class Solution:
    def diameterOfBinaryTree(self, root) -> int:
        self.best = 0

        def height(node) -> int:
            # returns height in EDGES; empty subtree = -1 so a leaf = 0
            if not node:
                return -1
            lh = height(node.left)
            rh = height(node.right)
            # best path that bends exactly here uses both arms
            self.best = max(self.best, lh + rh + 2)
            return max(lh, rh) + 1   # only ONE arm continues upward

        height(root)
        return self.best
```

The line to internalize: the **update** uses both arms, the **return** uses one. A path that bent at this node cannot bend again at the parent.

## 6. Complexity

- **Time O(n)** — "single post-order traversal; constant work per node once its children's heights return."
- **Space O(h)** recursion stack — "worst case O(n) on a chain, O(log n) when balanced."

## 7. Edge-case traps

- **Empty tree and single node** → 0; the `-1` null-height convention makes both fall out without guards.
- **Diameter avoiding the root** — `[1,2,null,3,4,5,null,6]`: the best path (`6-3-2-4` area) lives in the left subtree; any solution that only measures through the root returns 3 instead of 4.
- **Edges vs nodes** — off-by-one everywhere if the convention drifts mid-function; the tests distinguish 3 from 4 on several shapes.
- **Returning `lh + rh + 2` upward** instead of `max(lh, rh) + 1` — inflates ancestors' heights and overcounts; the full-tree case catches it.
- **Deep chain** — O(n²) rescans and default recursion limits both die here.

## 8. (DP section — not applicable)

Not DP (though it rhymes with it: child results are reused exactly once). The reusable template is the **post-order "return a summary up, update a global best at the bend"** pattern — the skeleton of Maximum Path Sum 124 and Longest Univalue Path 687.

## 9. Interviewer follow-up

- *"Weighted version: maximize the sum of node values on a path, values may be negative"* — Maximum Path Sum 124: return `max(0, best single arm + node.val)` upward (clamp: an arm is optional when negative), update with both arms + value.
- *"Count paths hitting a target sum instead of the longest one"* — that's Path Sum III 437, this problem's linked follow-up; the "summary" passed through the recursion becomes a running prefix-sum map instead of a height.
- *"Diameter of an n-ary tree"* — at each node keep the top two child heights; update with `top1 + top2 + 2`.
- *"Actual endpoints, not just the length?"* — return (height, deepest node) pairs and record the argmax pair at the best bend.
