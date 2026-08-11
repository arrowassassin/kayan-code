# Number of Connected Components in an Undirected Graph

You are given `n` nodes labeled `0` through `n - 1` and a list `edges`, where `edges[i] = [a, b]` is an undirected edge between nodes `a` and `b`.

Return the number of **connected components** — the number of groups of nodes such that every node in a group can reach every other node in the same group via edges, and no node can reach a node in a different group. A node with no edges forms a component by itself.

## Example 1

```
Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2
```

`{0,1,2}` is one component, `{3,4}` is the other.

## Example 2

```
Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1
```

A single chain links everyone.

## Constraints

- `1 <= n <= 2000`
- `0 <= len(edges) <= 5000`
- `edges[i] = [a, b]` with `0 <= a, b < n` and `a != b`
- No duplicate edges (in either orientation)
