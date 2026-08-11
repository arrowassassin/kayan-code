## Hint 1

"One node per depth" is the phrase to latch onto. Which traversal naturally organizes nodes by depth? And beware the shortcut of just walking `root.right` forever — what happens when a right subtree runs out before a deeper left one?

## Hint 2

If you had all nodes grouped level by level, the answer is just one element per group. You don't need to store the groups — you only need to recognize, mid-traversal, when you're at a level's final node.

## Hint 3

BFS level loop: snapshot `width = len(queue)`, pop `width` nodes; the node popped at index `width - 1` is the visible one. Alternatively DFS visiting right child first and recording the first node seen at each new depth — be ready to defend the recursion-depth implications of that choice.
