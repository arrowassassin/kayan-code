# TreeNode is predefined in the judge namespace: val / left / right.

class Codec:
    def serialize(self, root) -> str:
        parts = []

        def dfs(node):
            if not node:
                parts.append("#")  # explicit null marker makes shape unambiguous
                return
            parts.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(parts)

    def deserialize(self, data: str):
        tokens = iter(data.split(","))

        def build():
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))  # noqa: F821 - predefined by judge
            node.left = build()   # preorder: left subtree comes next
            node.right = build()
            return node

        return build()


# DO NOT EDIT below this line — the judge grades Codec via roundtrip.
class Solution:
    def roundtrip(self, root):
        codec = Codec()
        return codec.deserialize(codec.serialize(root))
