# Graph Valid Tree — Editorial

## 1. Pattern recognition

The statement literally hands you the definition to verify: **connected** and **acyclic**. Each half maps to a standard graph tool — connectivity is a single traversal's reach, cycle detection in an undirected graph is a traversal with parent tracking (or Union-Find). But the expert tell on this problem is a piece of *graph theory* that collapses the two checks into one: the edge-count characterization of trees. Interviewers use this question to see whether you verify definitions mechanically or notice structural shortcuts first.

## 2. Brute force first

Verify both properties independently: one BFS/DFS from node 0 counting reached nodes (connectivity), plus an undirected cycle check — DFS remembering each node's parent, flagging any visited neighbor that isn't the parent. That's O(V + E) and perfectly acceptable… but it's *two* subtle traversals, and undirected cycle detection carries a classic bug: without parent tracking, the edge you just walked (`a—b`, then seeing `a` from `b`) masquerades as a cycle, rejecting every graph with at least one edge. Note also that duplicate-edge inputs would break naive parent tracking — our constraints exclude them, which is worth *saying* you checked. The shortcut removes the entire minefield.

## 3. The key insight

**A graph on `n` nodes is a tree iff it has exactly `n - 1` edges and is connected — with the edge count pinned, acyclicity comes for free.**

## 4. Step-by-step derivation

1. Count first: a tree on `n` nodes has exactly `n - 1` edges. Fewer edges cannot connect `n` nodes; more edges must close a cycle. So `len(edges) != n - 1` → `false` in O(1), before building anything.
2. Why one check now suffices: a connected graph with `n - 1` edges cannot contain a cycle (a cycle wastes an edge that connectivity needs elsewhere — deleting one cycle edge keeps it connected, leaving `n - 2` edges connecting `n` nodes, impossible). State this implication aloud; it's the whole cleverness of the solution.
3. So: build the undirected adjacency list (both directions — the eternal discipline), BFS from node 0, count visited nodes, and return `seen == n`.
4. BFS vs DFS is indifferent here (no distances needed); use an iterative `deque`-based BFS because a valid tree can be a 2000-node path — exactly the depth that kills recursive DFS at Python's default limit. Mark visited on enqueue so no node is queued twice.
5. `n = 1` with zero edges falls out correctly: `0 == 1 - 1` passes the count, and the BFS trivially reaches the single node.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def validTree(self, n: int, edges: list[list[int]]) -> bool:
        # A tree on n nodes has EXACTLY n-1 edges. Fewer -> disconnected,
        # more -> cycle. With the count right, one check implies the other.
        if len(edges) != n - 1:
            return False

        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        # edge count is right: connectivity alone now proves tree-ness
        visited = [False] * n
        visited[0] = True
        queue = deque([0])
        seen = 1
        while queue:
            node = queue.popleft()
            for nb in adj[node]:
                if not visited[nb]:
                    visited[nb] = True
                    seen += 1
                    queue.append(nb)
        return seen == n
```

## 6. Complexity

- **Time O(V + E)** — "one pass to build adjacency, one traversal touching each node and edge once; with the count check, E is at most V-1 anyway."
- **Space O(V + E)** — "adjacency list plus O(V) visited array and queue."

## 7. Edge-case traps

- **`n = 1`, no edges** → `true`; an edge-count check written as `len(edges) < n - 1` only, or a BFS that assumes edges exist, stumbles here.
- **Right edge count, wrong shape** — `n = 4, edges = [[0,1],[1,2],[2,0]]`: a triangle plus an isolated node has exactly `n - 1 = 3` edges yet is disconnected (and cyclic). This is precisely why the connectivity BFS is still mandatory after the count check — the count alone proves nothing on its own.
- **Two nodes, no edge** → `false` by count; simple but frequently mishandled by "connected only" solutions that start and end at node 0.
- **Parent-tracking route** (if you skip the count trick): seeing the parent again is not a cycle; with duplicate edges allowed it *would* be — always state your assumption.
- **2000-node path** — the stress shape for recursion; iterative traversal sidesteps it.

## 8. Reusable template

Not DP. This trains the **connectivity-count BFS template** plus the tree edge-count fact — the same reachability sweep as Number of Connected Components, sharpened by an O(1) structural precheck.

## 9. Interviewer follow-up

- *"Edges arrive online; report tree-validity after each addition"* — Union-Find: an edge joining two nodes already in one set creates a cycle (reject or flag); the structure is a tree when exactly `n - 1` accepted unions have run. This is the canonical segue — be ready to code `find` with path compression.
- *"Find the redundant edge that breaks tree-ness"* — Redundant Connection (684): first edge whose endpoints already share a Union-Find root.
- *"Directed version: is it a rooted tree?"* — now you need every node except one to have indegree exactly 1, plus reachability from the root — the undirected shortcut does not transfer; that contrast is the point of asking.
