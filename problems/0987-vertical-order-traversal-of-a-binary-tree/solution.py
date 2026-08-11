from collections import defaultdict


class Solution:
    def verticalTraversal(self, root) -> list[list[int]]:
        cols = defaultdict(list)  # column -> [(row, val), ...]

        def dfs(node, row, col):
            if not node:
                return
            cols[col].append((row, node.val))
            dfs(node.left, row + 1, col - 1)
            dfs(node.right, row + 1, col + 1)

        dfs(root, 0, 0)
        # per column: sort by row, then by value to break same-cell ties
        return [[val for _, val in sorted(cols[c])] for c in sorted(cols)]
