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
