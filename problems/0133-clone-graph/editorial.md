# Clone Graph — Editorial

## 1. Pattern recognition

"Deep copy a linked structure that may contain cycles" is a **traversal-with-memory** problem. Copying a tree needs no memory — you can't revisit anything — but the word *graph* changes everything: node 1's neighbor list and node 3's neighbor list can both point at node 2, and a cycle means naive recursion never terminates. Whenever a structure can reach the same object by two routes, the pattern is: one traversal (BFS or DFS) plus a **map from original object to its copy** that is consulted before any object is created. The same idea solves Copy List with Random Pointer.

## 2. Brute force first

The naive recursion — "return a new node whose neighbors are clones of my neighbors" — with no bookkeeping either recurses forever on any cycle (even the 2-node graph `1—2`: cloning 1 clones 2, which clones 1, ...) or, with a per-path guard, duplicates shared nodes: two different routes to node 2 mint two distinct copies, so the clone has the wrong shape even when it terminates. This isn't a speed failure, it's a correctness failure — which is the interview point: the bottleneck is *identity*, not time.

## 3. The key insight

**Keep one dictionary `original -> clone`; create a copy only on first sight and look it up every time after — the map is simultaneously your visited set and your wiring table.**

## 4. Step-by-step derivation

1. Separate the two jobs: (a) create one fresh `Node` per original, (b) connect copies to copies. Both jobs need to answer "have I seen this original, and where is its copy?" — one hash map answers both (Python dicts hash objects by identity, which is exactly what we want here; using `val` as the key also works since values are unique).
2. Traverse from the start node. On popping `cur`, walk its edges: if `nb` is unseen, mint `clones[nb]` and enqueue `nb`; either way, append `clones[nb]` (never `nb` itself!) to `clones[cur].neighbors`.
3. Why this wires every edge exactly once per direction: each undirected edge appears in two adjacency lists, and we process each list once — so both directed halves get copied, preserving neighbor order.
4. BFS vs DFS: both are O(V + E). Recursion reads a touch cleaner, but a 100-node path already means depth 100, and the general pattern must survive graphs where depth ≈ V; in Python, the iterative `deque` version sidesteps recursion limits entirely — choose it and say why.
5. Handle `None` before touching `.val`: the empty graph is a legal input.

## 5. Annotated Python solution

```python
# Node is predefined: val/neighbors
from collections import deque


class Solution:
    def cloneGraph(self, node: "Node") -> "Node":
        if node is None:
            return None

        clones = {node: Node(node.val)}     # original -> its copy; doubles as visited
        queue = deque([node])
        while queue:
            cur = queue.popleft()
            for nb in cur.neighbors:
                if nb not in clones:        # first sighting: create copy, explore later
                    clones[nb] = Node(nb.val)
                    queue.append(nb)
                clones[cur].neighbors.append(clones[nb])   # wire copy to copy

        return clones[node]
```

## 6. Complexity

- **Time O(V + E)** — "each node is cloned once and each adjacency entry is walked once."
- **Space O(V)** — "the map holds every node, and the queue is bounded by V."

## 7. Edge-case traps

- **Null input** → return `None`; `clones[node]` on an empty map is the giveaway crash.
- **Single node, no neighbors** → the loop body never wires anything; the bare clone must still come back.
- **Appending the original neighbor** instead of its clone → the result *looks* right (same values) but shares objects with the input — a judge that checks structure passes it, a real deep-copy check does not. Say explicitly that no returned object may alias an input object.
- **Creating the clone on dequeue instead of first sighting** → two paths reach a node before it's dequeued and mint two copies; create-on-first-contact is the discipline.
- **Two-node cycle `1—2`** → the smallest input that infinite-loops the memoryless recursion; test it first.

## 8. Reusable template

Not DP. This trains the **traversal + original→copy map template** — the identical mechanism behind Copy List with Random Pointer and any deep-copy of a cyclic object graph.

## 9. Interviewer follow-up

- *"The graph may be disconnected and you get a list of entry nodes"* — run the same BFS from each entry, sharing one `clones` map so cross-references stay consistent.
- *"Directed graph?"* — nothing changes; each stored edge is copied once. The undirected symmetry was never assumed by the algorithm.
- *"Clone without O(V) extra space?"* — for graphs there's no clean trick, but mention the linked-list cousin: Copy List with Random Pointer interleaves copies with originals to replace the map — the interviewer is checking you know *why* that trick needs a linear structure.
