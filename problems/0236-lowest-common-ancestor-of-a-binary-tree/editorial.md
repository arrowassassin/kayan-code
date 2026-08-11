# Lowest Common Ancestor of a Binary Tree — Editorial

## 1. Pattern recognition

"Deepest node whose subtree contains both targets" is a question about **where two search results converge** — and convergence points in trees are found bottom-up. No BST ordering means no way to steer left or right ("values carry no ordering information" is the statement's explicit nudge), so the shape is: recurse everywhere, and have each subtree *report upward* what it found. This is the purest example of the "return info up" half of tree recursion — nothing is passed down at all; the entire algorithm lives in what flows up.

## 2. Brute force first

Two passes: DFS to record the root-to-`p` path and the root-to-`q` path (as lists of nodes), then walk both paths in lockstep and keep the last node where they agree. O(n) time, O(h) extra path storage — honestly, it's *fine*, and it's the right mental model for the answer. Its cost is aesthetic and practical: two traversals, explicit path plumbing, and it doesn't generalize to the one-pass form interviewers want. The single-pass version does the same "last agreement" computation implicitly, in one traversal, with no stored paths.

## 3. The key insight

**Have each subtree report the single target (or resolved LCA) it contains; the first node where both children's reports are non-empty is the LCA.**

## 4. Step-by-step derivation

1. Define `find(node)` → a node or `None`, meaning: "the LCA of whichever targets exist in this subtree — or the one target found, or nothing."
2. Base cases: `find(None) = None`; and if `node.val` is `p` or `q`, return `node` immediately — no need to search deeper, because if the other target is beneath it, this node is an ancestor of both, hence the LCA anyway (the "a node is its own ancestor" rule doing real work).
3. Otherwise recurse both children. Three outcomes: both non-`None` → the targets are split across the two subtrees, and this is the deepest node where that happens (any ancestor would see them merged into one side) → return `node`. Exactly one non-`None` → forward it. Both `None` → return `None`.
4. Why can one return value mean either "found just `p`" or "found the full LCA"? Because once both targets are seen, every ancestor above the split has exactly one non-`None` child report — the ambiguity never causes a wrong merge; the resolved LCA just rides up unchanged. That argument is the correctness proof and worth saying aloud.
5. Since `p` and `q` arrive as values, comparisons are `node.val == p`; uniqueness (guaranteed) is what makes that sound. Return `find(root).val` — the guarantee that both exist means `find(root)` is never `None`.
6. Recursion depth = tree height, up to 10^4 on the hidden chain — over CPython's default ~1000 limit (fine under this judge's raised limit). The iterative escape hatch: one traversal recording `parent` pointers into a dict, then climb from `p` collecting ancestors into a set, climb from `q` until the first hit. That's the brute-force idea rebuilt without recursion — knowing both is the interview-complete answer.

## 5. Annotated Python solution

```python
class Solution:
    def lowestCommonAncestor(self, root, p: int, q: int) -> int:
        def find(node):
            # reports: None = nothing here; else the target found here,
            # or the already-resolved LCA
            if not node or node.val == p or node.val == q:
                return node
            left = find(node.left)
            right = find(node.right)
            if left and right:      # targets split here -> deepest such node
                return node
            return left or right    # forward whatever one side found

        return find(root).val       # both targets guaranteed present
```

## 6. Complexity

- **Time O(n)** — "one post-order pass; every node inspected at most once."
- **Space O(h)** — "recursion stack only; O(n) worst case on a chain, O(log n) balanced."

## 7. Edge-case traps

- **One target is the other's ancestor** (`p=5, q=4` in the example) → answer is `p`; the early-return base case handles it *only if* you stop at a match instead of recursing past it.
- **Root is one of the targets** → answer is the root; also covered by the early return.
- **Adjacent parent–child pairs** (`[1,2]` and `[2,1]`) — smallest trees where direction matters.
- **Deep chain with both targets near the bottom** — recursion depth and any O(n·h) repeated-search approach both get stressed.
- **Assuming BST ordering** — steering by comparison silently returns a wrong node here; the tree is explicitly unordered.

## 8. (DP section — not applicable)

Not DP. Template trained: post-order **subtree reports** — a child summarizes "what of interest lives below me" and the parent combines two reports; the same shape solves Count Univalue Subtrees, Subtree of Another Tree, and Distribute Coins.

## 9. Interviewer follow-up

- *"What if `p` or `q` might be absent?"* — the early return becomes unsound (you'd report an LCA without confirming the other target). Fix: have `find` also count matches found, or post-verify with a containment check; return null when only one target exists. (This is LC 1644's twist.)
- *"Nodes have parent pointers?"* — climb from both nodes: set-of-ancestors, or the elegant two-pointer switcheroo (each pointer walks up and restarts at the other node; they meet at the LCA) — same trick as intersecting linked lists.
- *"Millions of (p, q) queries on a static tree?"* — precompute Euler tour + sparse table (RMQ) or binary lifting: O(n log n) preprocessing, O(1)–O(log n) per query.
- *"LCA of k nodes?"* — same recursion; return a node when ≥ 2 child reports (or a self-match) exist, or fold pairwise.
