## Hint 1

Write down the definition you need to verify: a tree is connected and acyclic. Before designing any traversal, is there a simple *counting* fact about how many edges a tree on `n` nodes must have?

## Hint 2

A tree has exactly `n - 1` edges. Fewer means disconnected; more forces a cycle. And once the edge count is exactly `n - 1`, connectivity and acyclicity become equivalent — so you only need to verify **one** of them.

## Hint 3

Check `len(edges) == n - 1` first (this also handles `n = 1` with no edges). Then build an undirected adjacency list and BFS/DFS from node 0, counting reached nodes; return whether the count equals `n`. If you instead skip the counting shortcut, you must detect cycles in an *undirected* graph — remember to track each node's parent so the edge you just came through doesn't look like a cycle.
