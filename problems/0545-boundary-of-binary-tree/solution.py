class Solution:
    def boundaryOfBinaryTree(self, root) -> list[int]:
        if not root:
            return []

        def is_leaf(n) -> bool:
            return not n.left and not n.right

        res = [root.val]          # root appears exactly once, up front
        if is_leaf(root):
            return res            # single-node tree: root is the whole boundary

        # 1) left boundary: from root.left, prefer left, fall back to right;
        #    leaves are skipped (the leaf pass owns them)
        node = root.left
        while node:
            if not is_leaf(node):
                res.append(node.val)
            node = node.left if node.left else node.right

        # 2) all leaves, left to right
        def add_leaves(n):
            if not n:
                return
            if is_leaf(n):
                res.append(n.val)
                return
            add_leaves(n.left)
            add_leaves(n.right)

        add_leaves(root)

        # 3) right boundary: from root.right, prefer right, fall back to left;
        #    collected top-down, emitted bottom-up
        stack = []
        node = root.right
        while node:
            if not is_leaf(node):
                stack.append(node.val)
            node = node.right if node.right else node.left
        res.extend(reversed(stack))

        return res
