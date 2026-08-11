# Course Schedule — Editorial

## 1. Pattern recognition

"Task X must happen before task Y" is the signature of a **directed dependency graph**, and "can everything be completed?" asks whether that graph can be linearized — i.e. whether it is a **DAG**. The moment a statement mentions prerequisites, build orders, or "A before B", think **topological sort / cycle detection**. Note the framing trick: the answer doesn't depend on *which* order you pick, only on whether *any* order exists, and the only obstruction is a directed cycle.

## 2. Brute force first

For each course, walk its prerequisite chains all the way down and see if you ever return to where you started — a fresh DFS per course with no shared bookkeeping. Each DFS can touch all E edges, so this is O(V·E) ≈ 2000 × 5000 = 10⁷ edge visits *per restart pattern*, and with path re-exploration in dense graphs it degrades further (exponential if you enumerate paths naively). It also re-proves the same subgraph acyclic over and over — the classic sign that one shared visited structure should replace per-node restarts.

## 3. The key insight

**All courses can be finished if and only if the prerequisite graph has no directed cycle — and a graph is acyclic exactly when you can repeatedly peel off nodes with indegree 0 until nothing remains.**

## 4. Step-by-step derivation

1. Build adjacency the *unlocking* direction: for `[a, b]`, add edge `b -> a`. Getting this backwards doesn't change cycle-existence, but say the direction out loud anyway — the follow-up (returning an actual order) breaks if it's flipped.
2. A course with indegree 0 has no unmet prerequisites; it can be taken immediately. Taking it removes its outgoing edges, possibly freeing others. That peeling process is **Kahn's algorithm** — BFS where the queue holds "currently takeable" courses.
3. Why it detects cycles: a cycle's members all have an incoming edge *from within the cycle*, so none of them ever reaches indegree 0. The peeling stalls with them un-taken. Hence: `taken == numCourses` ⇔ acyclic.
4. The DFS alternative — three colors (white unvisited, gray on the current stack, black finished); a gray→gray edge is a cycle. It's equally correct, but in Python prefer the iterative BFS: no recursion-limit worries at V = 2000+ chain depth, and the visited discipline is simpler (a node enters the queue exactly once, at the moment its indegree hits 0).
5. Either way, every node and edge is processed once: O(V + E).

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        # edge b -> a: b unlocks a
        adj = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indegree[a] += 1

        # Kahn's algorithm: start from courses with no prerequisites
        queue = deque(c for c in range(numCourses) if indegree[c] == 0)
        taken = 0
        while queue:
            course = queue.popleft()
            taken += 1
            for nxt in adj[course]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:      # last prerequisite just cleared
                    queue.append(nxt)

        return taken == numCourses          # anyone left is stuck in a cycle
```

## 6. Complexity

- **Time O(V + E)** — "each course is enqueued once and each prerequisite edge is relaxed once."
- **Space O(V + E)** — "the adjacency list dominates; the queue and indegree array are O(V)."

## 7. Edge-case traps

- **No prerequisites at all** → trivially `true`; make sure an empty edge list builds a valid (all-zero) indegree array.
- **Self-loop** `[1,1]` → indegree never reaches 0 for that course; `false`. A DFS that only checks *neighbors* for gray can miss this if the node isn't marked gray before exploring.
- **Cycle in one component, clean courses elsewhere** → the clean ones all get taken; the count check still says `false`. Returning "queue emptied" instead of comparing counts is the classic bug.
- **`[a, b]` direction confusion** — harmless here, fatal in Course Schedule II; build `b -> a` now so the follow-up is a three-line diff.
- **Deep chain (2000 nodes)** — recursive DFS flirts with Python's recursion limit; the iterative Kahn version is immune, and saying so is interview credit.

## 8. Reusable template

Not DP. This trains the **Kahn indegree-peeling template** for topological sort and cycle detection — reused verbatim in Course Schedule II, Alien Dictionary, and Minimum Height Trees.

## 9. Interviewer follow-up

- *"Now return an actual order to take the courses"* — Course Schedule II (210), the linked follow-up: identical loop, just append each popped course to an output list.
- *"Which courses are impossible?"* — the ones never taken: `[c for c in range(numCourses) if indegree[c] > 0]` after peeling (indegree-0 leftovers can't occur).
- *"Prerequisites arrive as a stream — recheck after each insert?"* — incremental cycle detection is genuinely hard; the honest answer is re-running Kahn (O(V+E) per insert) and mentioning that dynamic topological-order maintenance is a known research-grade structure.
