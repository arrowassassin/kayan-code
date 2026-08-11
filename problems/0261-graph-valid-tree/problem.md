# Graph Valid Tree

You are given `n` nodes labeled `0` through `n - 1` and a list `edges`, where `edges[i] = [a, b]` is an undirected edge between nodes `a` and `b`.

Decide whether these nodes and edges form a **valid tree** — that is, the graph is **connected** and contains **no cycle**.

Return `true` if it is a valid tree, `false` otherwise.

## Example 1

```
Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
Output: true
```

All five nodes hang together and no edge closes a loop.

## Example 2

```
Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
Output: false
```

`1 -> 2 -> 3 -> 1` is a cycle.

## Example 3

```
Input: n = 2, edges = []
Output: false
```

Two nodes with no edge between them are disconnected.

## Constraints

- `1 <= n <= 2000`
- `0 <= len(edges) <= 5000`
- `edges[i] = [a, b]` with `0 <= a, b < n` and `a != b`
- No duplicate edges (in either orientation)
