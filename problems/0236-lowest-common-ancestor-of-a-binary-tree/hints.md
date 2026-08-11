## Hint 1

Without BST ordering you can't steer the search — you have to look everywhere. Think about what a subtree could usefully *report* to its parent about the two targets.

## Hint 2

For any node there are only three interesting situations: both targets are below it in different children's subtrees, both are below it on the same side, or one of them *is* this node. Which of these pins the node as the answer?

## Hint 3

Post-order recursion returning a node: return the current node if it matches `p` or `q`; otherwise recurse both sides. If both sides return something, the targets split here — this node is the LCA. If one side returns something, forward it upward unchanged. Convince yourself why "found `p` only" and "found the finished LCA" can share one return value.
