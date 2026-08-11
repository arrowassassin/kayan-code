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
