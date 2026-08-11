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
