# Clone Graph

You are handed a reference to one node of a **connected undirected graph**. Each node carries an integer value and a list of neighbor nodes:

```
class Node:
    val: int
    neighbors: list[Node]
```

Build and return a **deep copy** of the entire graph: every node must be a newly created object, and the copied nodes must be wired to each other exactly as the originals are. No node in the returned graph may be an object from the input graph.

Node values are unique and equal to each node's 1-based index (node 1 has `val = 1`, and the given reference is node 1). The test format describes the graph as an adjacency list: entry `i` lists the values of node `i+1`'s neighbors.

## Example 1

```
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
```

A 4-cycle: node 1 touches 2 and 4, node 2 touches 1 and 3, and so on. The clone has the same shape built from fresh objects.

## Example 2

```
Input: adjList = [[]]
Output: [[]]
```

One lonely node with no neighbors — the clone is a single new node.

## Example 3

```
Input: adjList = []
Output: []
```

The graph is empty (the reference is null); return null.

## Constraints

- `0 <= number of nodes <= 100`
- `1 <= Node.val <= 100`, all values unique
- No self-loops and no repeated edges; the graph is connected
- Edges are symmetric: if `u` lists `v`, then `v` lists `u`
