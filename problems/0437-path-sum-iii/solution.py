from collections import defaultdict


class Solution:
    def pathSum(self, root, targetSum: int) -> int:
        seen = defaultdict(int)   # prefix sum -> count on current root path
        seen[0] = 1               # empty prefix: paths starting at the root
        self.count = 0

        def dfs(node, running):
            if not node:
                return
            running += node.val
            # a path ending here sums to target iff some ancestor prefix
            # equals running - target
            self.count += seen[running - targetSum]
            seen[running] += 1
            dfs(node.left, running)
            dfs(node.right, running)
            seen[running] -= 1    # backtrack: leave no trace for siblings

        dfs(root, 0)
        return self.count
