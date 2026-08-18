# Boundary of Binary Tree — Editorial

## 1. Pattern recognition

The statement itself is a specification in four numbered pieces: root, left edge, leaves, right edge reversed. That's the signal. This is not a "find the clever traversal" problem — it's a **decomposition** problem. Trying to produce the boundary in one traversal (tracking "am I currently on the boundary?" flags through a single DFS) is exactly how candidates drown: the flag logic has four interacting states and the leaf/edge overlap cases turn into whack-a-mole. This is a ★ top-priority question, and what it really tests is whether you can turn a fussy spec into three tiny, boring passes — plus whether you nail the ownership rules that prevent duplicates.

## 2. Brute force first

There's no asymptotically-worse brute force to beat here — any correct answer is O(n) because you must at least look at every leaf. The "brute force" failure mode is *structural*: one mega-traversal with boundary flags, or computing the three lists and then de-duplicating by value. De-duplicating by value is wrong outright (values repeat; the constraint says so), and the flag traversal is where the 40-minute clock dies. Cost of the clean decomposition: three passes, each trivially O(n).

## 3. The key insight

**Assign each boundary node exactly one owner — root pass, leaf pass, or side pass — and make the side walks skip every leaf, so the pieces are disjoint by construction and simply concatenate.**

## 4. Step-by-step derivation

1. Emit `root.val` first. If the root is a leaf, stop — otherwise the leaf pass may not touch the root (piece 3's rule), and the side walks start strictly below it, so the root can never reappear.
2. **Left boundary** is a *walk*, not a search: from `root.left`, go `left` if possible else `right`. This "hug the left wall" rule is the definition; a plain leftmost-descent would fall off the tree the moment a node lacks a left child. Append non-leaf values only — the bottom of this walk is always a leaf, and the leaf pass owns it.
3. **Leaves** are one recursive DFS, visiting left before right so leaves come out left-to-right. This pass is the classic "return info up" shape in its simplest form — no info even needs returning, just an append at each leaf. (Recursive is fine here: depth ≤ 10^4 and the judge's recursion limit is far above that; in stock CPython you'd call `sys.setrecursionlimit` first or switch to an explicit stack.)
4. **Right boundary** is the mirror walk from `root.right` (prefer `right`, else `left`) — but the spec wants it bottom-up. Collect top-down into a stack and extend the result with its reversal. Symmetric code, one `reversed()`.
5. Disjointness argument, since the interviewer will ask: the side walks exclude leaves and the root; the leaf pass emits only leaves and never the root; the root is emitted once, manually. No overlaps possible, so concatenation is the answer.

## 5. Annotated Python solution

```python
class Solution:
    def boundaryOfBinaryTree(self, root) -> list[int]:
        if not root:
            return []

        def is_leaf(n) -> bool:
            return not n.left and not n.right

        res = [root.val]          # root appears exactly once, up front
        if is_leaf(root):
            return res            # single-node tree: root is the whole boundary

        # 1) left boundary: prefer left, fall back to right; skip leaves
        node = root.left
        while node:
            if not is_leaf(node):
                res.append(node.val)
            node = node.left if node.left else node.right

        # 2) all leaves, left to right
        def add_leaves(n):
            if not n:
                return
            if is_leaf(n):
                res.append(n.val)
                return
            add_leaves(n.left)
            add_leaves(n.right)

        add_leaves(root)

        # 3) right boundary: prefer right, fall back to left;
        #    collected top-down, emitted bottom-up
        stack = []
        node = root.right
        while node:
            if not is_leaf(node):
                stack.append(node.val)
            node = node.right if node.right else node.left
        res.extend(reversed(stack))

        return res
```

## 6. Complexity

- **Time O(n)** — "two O(h) wall walks plus one full DFS for the leaves; every node is touched a constant number of times."
- **Space O(h)** for the DFS recursion stack and the right-boundary stack — "output aside, it's bounded by the tree's height."

## 7. Edge-case traps

- **Single-node tree** → `[root]`, not `[root, root]` — the root must not also be counted as a leaf.
- **Root with only one child** — e.g. `[1,2]` → `[1,2]`: the child is a leaf, so it appears via the leaf pass; the empty side must contribute nothing.
- **Left boundary that bends right** (`[1,2,null,null,3]`) — the fall-back rule matters; leftmost-only descent misses node 3's path.
- **Right boundary that bends left** (`[1,2,3,null,null,4,null]`) — mirror trap, plus the reversal.
- **Skewed chains** — a left chain's boundary is the whole tree in order; a right chain of `1→2→3` gives `[1,3,2]` (leaf before the reversed edge).
- **Duplicate values** — any de-dup-by-value "fix" fails; correctness must come from structure.

## 8. (DP section — not applicable)

Not DP. The reusable template is **decompose-by-specification**: several trivial traversals with explicit ownership rules beat one traversal with state flags — the same instinct that untangles matrix-spiral and zigzag-format problems.

## 9. Interviewer follow-up

- *"Do it in one traversal anyway."* — Possible: DFS passing down two booleans (`on_left_edge`, `on_right_edge`); a child inherits left-edge status if it's the left child of a left-edge node (or the fallback child when the left is absent), mirrored for the right; collect into three buffers as you go. Good candidates say clearly that they'd write the three-pass version under time pressure and sketch this only if asked.
- *"Clockwise instead?"* — Swap the roles: right boundary top-down first, leaves right-to-left, left boundary reversed.
- *"Boundary of an n-ary tree?"* — Left wall = always-first-child walk, right wall = always-last-child walk, leaves = nodes with no children; same ownership discipline.
