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
