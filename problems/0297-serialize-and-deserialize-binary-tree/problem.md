# Serialize and Deserialize Binary Tree

Design a codec that converts a binary tree to a single string and back, such that deserializing a serialized tree reconstructs the **exact original structure and values**.

Implement a class `Codec` with two methods:

- `serialize(root) -> str` — encode the tree into one string. You choose the format; there are no restrictions beyond it being a string.
- `deserialize(data) -> root` — decode that string back into an identical tree.

The only requirement is the round trip: `deserialize(serialize(root))` must reproduce the input tree exactly, for every valid tree — including the empty one. The judge grades exactly that round trip (via the provided `roundtrip` wrapper — do not edit it).

## Example 1

```
Input: root = [1,2,3,null,null,4,5]

    1
   / \
  2   3
     / \
    4   5

Round trip output: [1,2,3,null,null,4,5]
```

One workable encoding of this tree is the preorder string `"1,2,#,#,3,4,#,#,5,#,#"` — but any reversible format is accepted.

## Example 2

```
Input: root = []
Round trip output: []
```

## Constraints

- `0 <= number of nodes <= 10^4`
- `-1000 <= Node.val <= 1000` (values may be negative and are **not** unique)
- The tree may be a chain of `10^4` nodes — your codec must survive extreme skew.
- Statefulness between `serialize` and `deserialize` is cheating: `deserialize` must work from the string alone.
