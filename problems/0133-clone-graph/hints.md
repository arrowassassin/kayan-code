## Hint 1

Copying a tree is easy because you never revisit a node. What goes wrong if you apply the same naive "copy me, then copy my neighbors" recursion to a graph with a cycle?

## Hint 2

You need to create each node's copy exactly once and *find it again* every later time an edge points at it. What structure maps an original node to its already-made clone? That same map can double as your visited set.

## Hint 3

Traverse from the start node (BFS with a deque avoids recursion-depth worries). On first meeting a node, create its bare clone and store `clones[original] = copy`. When processing an edge `cur -> nb`, append `clones[nb]` to `clones[cur].neighbors` — never the original `nb`. Return `clones[start]`, and handle a null input up front.
