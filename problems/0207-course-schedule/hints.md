## Hint 1

Model courses as nodes and each prerequisite `[a, b]` as a directed edge `b -> a` ("b unlocks a"). When is it impossible to finish everything? Think about what shape in the graph creates a deadlock.

## Hint 2

All courses can be finished **exactly when the directed graph has no cycle**. So the task reduces to directed-cycle detection. Two standard tools: DFS with three node colors (unvisited / in-progress / done), or a BFS that repeatedly removes nodes with no incoming edges.

## Hint 3

Kahn's algorithm: compute each node's indegree, enqueue all indegree-0 nodes, and repeatedly pop one, "taking" it and decrementing the indegree of every course it unlocks — enqueue any that drop to 0. Count the pops. If you took all `numCourses` courses, there is no cycle; anything left over is trapped in one.
