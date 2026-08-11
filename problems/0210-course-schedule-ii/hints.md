## Hint 1

You already solved the decision version (Course Schedule). What extra information does your cycle-detection algorithm compute *for free* while it runs?

## Hint 2

In Kahn's algorithm, a course only enters the queue once its indegree hits 0 — i.e. once every prerequisite has already been popped. So the sequence of pops is itself a schedule that respects all prerequisites.

## Hint 3

Run Kahn exactly as before, but append each popped course to a result list. If the list ends up shorter than `numCourses`, a cycle blocked the rest — return `[]`. (DFS also works: post-order finish times, reversed, give a topological order — but you must still detect gray-edge cycles, and Python's recursion limit favors the iterative BFS.)
