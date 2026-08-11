class Solution:
    def lowestCommonAncestor(self, root, p: int, q: int) -> int:
        def find(node):
            # returns the LCA node of whichever targets live in this subtree,
            # or None if neither is here
            if not node or node.val == p or node.val == q:
                return node
            left = find(node.left)
            right = find(node.right)
            if left and right:  # one target on each side -> this is the split
                return node
            return left or right

        return find(root).val
