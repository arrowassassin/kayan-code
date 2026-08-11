# Validate Binary Search Tree — Editorial

## 1. Pattern recognition

The definition itself is the clue: the BST property speaks about **entire subtrees** ("every value in the left subtree…"), not parent–child pairs — and the statement bolds exactly that. A property that every node must satisfy *relative to its ancestors* calls for recursion that **passes constraints down**: each recursive call carries a summary of everything the ancestors demand. This is the mirror image of problems like Diameter 543, which pass *nothing* down and return summaries *up* — the two halves of tree recursion, and this problem is the canonical drill for the top-down half.

## 2. Brute force first

Two classic non-answers and one honest brute force. Non-answer #1: check `left.val < node.val < right.val` locally at each node — wrong, `[5,4,6,null,null,3,7]` passes it while `3` violates the root. Non-answer #2 is subtler and appears in real interviews: recompute, at every node, the max of its left subtree and min of its right subtree — correct but O(n·h), up to O(n²) work of repeated subtree scans. The honest baseline that's actually fine: inorder-traverse into a list and check it's strictly increasing — O(n) time but O(n) extra space and a second pass. All three point at the same question: can one pass with O(h) state do it?

## 3. The key insight

**Every ancestor's demand on a node compresses into one open interval `(low, high)` — turning left tightens the ceiling, turning right tightens the floor.**

## 4. Step-by-step derivation

1. Which values may legally appear at some position? Trace the path from the root: each left turn under a node `a` promises "everything here is `< a.val`"; each right turn promises "` > a.val`". The tightest ceiling is the *nearest ancestor you turned left under*; the tightest floor the nearest you turned right under.
2. So the recursion needs only `(low, high)`: check `low < node.val < high`, then recurse left with `(low, node.val)` and right with `(node.val, high)` — the current node becomes the new ceiling on one side and the new floor on the other. Everything older is already implied.
3. Initialize with `float('-inf')`/`float('inf')` rather than integer sentinels like ±2^31: node values legitimately hit both 32-bit extremes (the tests include `[-2147483648, null, 2147483647]`), and a sentinel *equal* to a real value falsely rejects it under strict comparison.
4. Strictness: the spec forbids duplicates, so both comparisons are strict; `[2,2,2]` must fail. If a variant permitted duplicates on one side, exactly one comparison would loosen — knowing *which* is a nice probe question.
5. The equally-valid alternative: inorder traversal keeping only the previous value, failing whenever `prev >= current`. Same O(n)/O(h), and it converts naturally to an explicit stack — the practical answer to "your tree is a 10^4-deep chain and CPython's default recursion cap is ~1000" (the judge raises the limit, so the recursive form passes here; say the caveat anyway).

## 5. Annotated Python solution

```python
class Solution:
    def isValidBST(self, root) -> bool:
        def valid(node, low, high) -> bool:
            # (low, high) = tightest ancestor demands, an OPEN interval
            if not node:
                return True
            if not (low < node.val < high):
                return False
            # left: this node becomes the new ceiling; right: the new floor
            return (valid(node.left, low, node.val)
                    and valid(node.right, node.val, high))

        return valid(root, float("-inf"), float("inf"))
```

## 6. Complexity

- **Time O(n)** — "every node is checked exactly once against two bounds."
- **Space O(h)** — "just the recursion stack: O(n) for a chain, O(log n) balanced."

## 7. Edge-case traps

- **Deep violation** — `[5,4,6,null,null,3,7]`: the case that executes local-check solutions; `3` is fine against `6` but not against `5`.
- **Duplicates** — `[2,2,2]`, `[1,null,1]`: strict `<` must reject; `<=` anywhere lets them through.
- **Extreme 32-bit values** — kills integer-sentinel initializations; use ±inf or `None`-means-unbounded.
- **Empty tree / single node** → valid; the null base case covers both.
- **Skewed valid chain of 10^4** — stresses recursion depth and any O(n·h) re-scanning approach.

## 8. (DP section — not applicable)

Not DP. Template trained: **pass-constraints-down recursion** — ancestors' demands compressed into small parameters — the same shape as bounds-checked trie walks and range-limited BST queries, and the complement of 543's return-info-up.

## 9. Interviewer follow-up

- *"Find the two swapped nodes in an almost-BST and fix them"* — Recover BST 99: inorder with a `prev` pointer; the first inversion's left element and last inversion's right element are the swapped pair.
- *"Validate a stream too large for recursion"* — iterative inorder with an explicit stack, keeping only `prev`; O(h) memory, no recursion limit.
- *"Duplicates allowed in the left subtree?"* — loosen exactly the ceiling check to `<=` (i.e. left recursion keeps `high = node.val` but the node test becomes `low < val <= high` on that side); be precise about which side your spec chooses.
- *"Count how many subtrees are BSTs"* — flip to return-info-up: each subtree returns (isBST, min, max), combined bottom-up — nice demonstration that the same property can be verified in either direction of the duality.
