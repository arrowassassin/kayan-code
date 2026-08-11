class Solution:
    def isValidBST(self, root) -> bool:
        def valid(node, low, high) -> bool:
            # every ancestor turn tightens one side of the open interval
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return (valid(node.left, low, node.val)
                    and valid(node.right, node.val, high))

        return valid(root, float("-inf"), float("inf"))
