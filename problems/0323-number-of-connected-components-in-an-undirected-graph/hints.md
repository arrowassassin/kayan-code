## Hint 1

This is Number of Islands without the grid: the adjacency is handed to you as an edge list instead of being implied by neighboring cells. What did the outer loop in the islands solution count, exactly?

## Hint 2

Every time you encounter a node that no previous traversal has touched, you have discovered a new component. Traverse from it and mark everything reachable so it is never counted again. You'll need to convert the edge list into an adjacency list first — and remember the edges are undirected.

## Hint 3

Build `adj` with both `a -> b` and `b -> a`. Loop `start` over all `n` nodes: if unvisited, increment the count and run an iterative DFS (explicit stack) or BFS from it, marking nodes visited as you push them. Isolated nodes never appear in `edges`, which is exactly why the outer loop must run over `range(n)` rather than over the edge list.
