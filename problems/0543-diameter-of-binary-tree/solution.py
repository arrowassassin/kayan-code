class Solution:
    def diameterOfBinaryTree(self, root) -> int:
        self.best = 0

        def height(node) -> int:
            # returns height in EDGES of the subtree rooted here
            if not node:
                return -1
            lh = height(node.left)
            rh = height(node.right)
            # path bending at this node uses both arms
            self.best = max(self.best, lh + rh + 2)
            return max(lh, rh) + 1

        height(root)
        return self.best
