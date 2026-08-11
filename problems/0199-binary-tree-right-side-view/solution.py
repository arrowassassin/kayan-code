from collections import deque


class Solution:
    def rightSideView(self, root) -> list[int]:
        if not root:
            return []
        res = []
        queue = deque([root])
        while queue:
            width = len(queue)
            for i in range(width):
                node = queue.popleft()
                if i == width - 1:  # last node of this level = visible one
                    res.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return res
