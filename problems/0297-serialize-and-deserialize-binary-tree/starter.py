# TreeNode is predefined: val / left / right.

class Codec:
    def serialize(self, root) -> str:
        """Encode a tree to a single string."""
        pass

    def deserialize(self, data: str):
        """Decode your string back to the identical tree; return its root."""
        pass


# DO NOT EDIT below this line — the judge grades Codec via roundtrip.
class Solution:
    def roundtrip(self, root):
        codec = Codec()
        return codec.deserialize(codec.serialize(root))
