# Course Schedule II — Editorial

## 1. Pattern recognition

This is the constructive twin of Course Schedule (the linked warmup): same directed dependency graph, but "return an ordering" instead of "return whether one exists". The phrase "any valid ordering" is itself a signal — problems that accept many answers are almost always asking you to *materialize* the certificate your decision algorithm already produced implicitly. Here that certificate is a **topological order**.

## 2. Brute force first

Repeatedly scan all courses for one whose prerequisites are all already taken; take it; repeat. Each scan is O(V + E) and you do V scans → O(V·(V + E)) ≈ 2000 × 7000 = 1.4 × 10⁷ — borderline in Python, and conceptually wasteful: after taking a course, only *its* dependents can change state, yet the rescan re-checks everyone. Trying all V! orderings is obviously absurd. The fix is bookkeeping that tells you *which* courses just became available.

## 3. The key insight

**Kahn's peeling order is itself a topological order — a course is popped only after every one of its prerequisites was popped, so recording the pops answers the question.**

## 4. Step-by-step derivation

1. Start from the Course Schedule solution: adjacency `b -> a` ("b unlocks a"), indegree array, queue of indegree-0 courses.
2. Prove the pop-order claim to yourself (and your interviewer): a course enters the queue only when its indegree hits 0, which happens only after each of its prerequisites was popped and decremented it. So by the time it's popped, all prerequisites appear earlier in the pop sequence. That's the definition of a topological order.
3. Therefore the entire diff from the warmup is: `order.append(course)` on pop, and `return order if len(order) == numCourses else []`. The count check still doubles as cycle detection — cycle members never reach indegree 0, so they never appear, and a short list means "impossible".
4. Edge direction now *matters*. In the boolean version a flipped adjacency still detects the cycle; here it silently emits the exact reverse order. Test with `[[1,0]]`: the answer must start with 0.
5. The DFS route also works — reversed post-order finish times — but it needs the three-color gray-edge check for cycles *and* an explicit stack (or raised recursion limit) for the 2000-deep chain. In an interview, name both, then pick iterative Kahn for Python and say why.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        # edge b -> a: b unlocks a
        adj = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indegree[a] += 1

        queue = deque(c for c in range(numCourses) if indegree[c] == 0)
        order = []
        while queue:
            course = queue.popleft()
            order.append(course)            # pop order IS a topological order
            for nxt in adj[course]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        return order if len(order) == numCourses else []
```

## 6. Complexity

- **Time O(V + E)** — "each course is popped once and each prerequisite edge is decremented once."
- **Space O(V + E)** — "adjacency list plus the O(V) queue, indegree array, and output."

## 7. Edge-case traps

- **Reversed adjacency** — the killer bug unique to this version: output is a valid order of the *reversed* graph, i.e. exactly wrong. `[[1,0]] -> [1,0]` instead of `[0,1]`.
- **Cycle present** → must return `[]`, not the partial order accumulated before the stall.
- **No prerequisites** → any permutation is valid; make sure you emit all `numCourses` courses, not just the ones with edges.
- **Self-loop** `[1,1]` → that course never unlocks; correct answer `[]`.
- **DFS variant without reversing post-order** — emits dependencies *after* dependents; if you go the DFS route, the `reversed()` at the end is load-bearing.

## 8. Reusable template

Not DP. This trains the **topological-sort-with-output template** (Kahn + pop log) — the direct engine behind Alien Dictionary and any build-order / task-scheduling question.

## 9. Interviewer follow-up

- *"Courses have durations; minimize total completion time with unlimited parallelism"* — longest path in the DAG: process in topological order, `finish[c] = duration[c] + max(finish of prerequisites)` (this is Parallel Courses III).
- *"Return the lexicographically smallest valid order"* — swap the queue for a min-heap; same peeling, O(V log V + E).
- *"Count the number of distinct valid orders"* — #P-hard in general; the expected answer is recognizing that, then handling small V by DP over subsets.
