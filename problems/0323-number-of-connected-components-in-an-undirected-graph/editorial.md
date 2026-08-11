# Number of Connected Components in an Undirected Graph — Editorial

## 1. Pattern recognition

"How many groups?" over an undirected relation is the textbook **connected components** count — Number of Islands with the costume removed. The one structural difference from grid problems is that the adjacency isn't implicit anymore: you're given an **edge list**, and step zero of nearly every edge-list problem is converting it to an **adjacency list**. Recognize also the fork in the road this problem offers: traversal (BFS/DFS) or Union-Find both fit; interviewers often ask this question precisely to hear you compare them.

## 2. Brute force first

Without adjacency lists, a traversal that finds a node's neighbors by scanning the whole edge list costs O(E) per node — O(V·E) = 2000 × 5000 = 10⁷ pair inspections, each with list indexing overhead; sluggish in Python and structurally wasteful, since every scan re-reads edges that will never again be relevant. Even worse is the "merge sets repeatedly until stable" simulation: start with each node alone, sweep the edges merging groups, repeat until no sweep changes anything — up to O(V) sweeps of O(E) merges. Both die to the same medicine: index the edges once, up front.

## 3. The key insight

**Each traversal started from an unvisited node consumes exactly one whole component — so the answer is simply the number of times you have to start.**

## 4. Step-by-step derivation

1. Build `adj` in O(E). The mandatory habit for undirected inputs: insert **both** `a -> b` and `b -> a`. Forgetting the reverse edge makes reachability directional and silently overcounts components.
2. Keep a `visited` array. Sweep `start` over all `n` labels — over the *labels*, not the edge list, or isolated nodes (which appear in no edge) are never counted.
3. On hitting an unvisited node: that's a component no previous traversal touched (traversals exhaust whole components — that's the invariant). Increment the counter and flood from it.
4. Flood with an explicit stack (iterative DFS) or a deque (BFS) — interchangeable here since no distances are needed. In Python, prefer iterative: a 2000-node path is exactly the shape that overruns default recursion limits, and saying "I'll use an explicit stack so depth can't bite me" is free interview credit.
5. Mark visited **when pushing**, not when popping — the same discipline as every problem in this topic; marking on pop lets a node enter the stack via two neighbors and inflates work.
6. Total: O(V + E) — each node pushed once, each edge relaxed twice.

## 5. Annotated Python solution

```python
class Solution:
    def countComponents(self, n: int, edges: list[list[int]]) -> int:
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)        # undirected: store BOTH directions
            adj[b].append(a)

        visited = [False] * n
        count = 0
        for start in range(n):
            if visited[start]:
                continue
            count += 1              # unseen node = brand-new component
            stack = [start]         # iterative DFS: no recursion limit worries
            visited[start] = True
            while stack:
                node = stack.pop()
                for nb in adj[node]:
                    if not visited[nb]:
                        visited[nb] = True      # mark on push, not on pop
                        stack.append(nb)
        return count
```

## 6. Complexity

- **Time O(V + E)** — "building adjacency touches each edge once; the traversals visit each node once and cross each edge twice."
- **Space O(V + E)** — "the adjacency list dominates; visited array and stack are O(V)."

## 7. Edge-case traps

- **Isolated nodes** — `n = 4, edges = []` must return 4; iterating over edges instead of `range(n)` returns 0.
- **One-directional adjacency** — the classic undirected-graph bug; the chain test `[[0,1],[1,2],[2,3],[3,4]]` still passes by luck of orientation, but reversed edges like `[[1,0]]` expose it.
- **Cycles** — `[[0,1],[1,2],[2,0]]` is still one component; without visited-on-push the stack churns.
- **2000-node path** (the stress test) — recursive DFS raises `RecursionError` at default limits; the explicit stack shrugs.
- **`n = 1`, no edges** — the minimal answer 1; loops must handle a graph with no adjacency at all.

## 8. Reusable template

Not DP. This trains the **component-counting sweep template** — "for each unvisited node: count += 1, flood" — the abstract core of Number of Islands, Graph Valid Tree's connectivity half, and Friend Circles.

## 9. Interviewer follow-up

- *"Edges arrive as a stream and you must answer the count after each insertion"* — this is where **Union-Find** beats traversal: keep a component counter, decrement whenever a union joins two distinct roots; with path compression + union by rank each operation is near-O(1) amortized. Being able to *contrast* the two solutions is the real point of this question.
- *"Return the size of each component"* — carry a per-flood counter, or read off Union-Find root sizes.
- *"Are nodes `a` and `b` connected?"* many times offline — either precompute component ids in one sweep and compare, or Union-Find; both give O(1) queries after linear prep.
