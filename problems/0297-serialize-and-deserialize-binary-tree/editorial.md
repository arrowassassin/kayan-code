# Serialize and Deserialize Binary Tree — Editorial

## 1. Pattern recognition

"Design a reversible encoding" flips the usual direction of tree problems: instead of extracting an answer from a structure, you must design a representation whose **decode is forced** — every byte you emit should leave the decoder zero choices. The classic fact lurking underneath: a preorder value sequence alone is ambiguous (`[1,2]` could be a left chain or a right chain), and CS-students' reflex "store preorder + inorder" fails here anyway because values repeat. The pattern to reach for is *traversal + explicit structure markers*: once nulls are written down, one traversal is enough.

## 2. Brute force first

Two tempting shortcuts. (a) Serialize preorder and inorder sequences, reconstruct classically — broken by duplicate values (`[2,2,2,...]` is in the hidden suite precisely for this), and O(n²) reconstructions are common. (b) Level-order array with nulls, LeetCode-input style — actually *correct* and interview-acceptable, but naive implementations pad ~2^h slots for skewed trees (the 10^4-chain test makes that 2^10000 — instant death) unless you strip trailing nulls / stop at the frontier. The clean statement of why markers beat both: they make the format *self-delimiting*, so decoding is a single linear consume with no searching and no index arithmetic.

## 3. The key insight

**Preorder with an explicit null marker per empty child is uniquely decodable: the decoder consumes tokens left to right, and each token tells it exactly whether to make a node or close a branch.**

## 4. Step-by-step derivation

1. Why is plain preorder ambiguous? Because the decoder can't tell where the left subtree ends. Emitting `#` for every `None` supplies exactly that boundary: a subtree's encoding is `val, <left encoding>, <right encoding>`, with `#` as the base case — a grammar with no lookahead needed.
2. **Encode**: preorder DFS appending tokens to a list, `",".join` once at the end. (Building the string with `+=` inside the recursion is O(n²) — a real TLE risk at 10^4 nodes, and worth flagging out loud.)
3. **Decode**: split into tokens and wrap them in a *shared iterator*. `build()` = take next token; `#` → `None`; else create the node, then `node.left = build()`, `node.right = build()`. No indices to pass around: the iterator's position **is** the recursion state, which is exactly why the left subtree's consumption leaves the iterator pointing at the right subtree's first token.
4. Correctness in one line: the encoding of a tree is `val · enc(L) · enc(R)` with `enc(∅) = #`, and `build` inverts each production deterministically — induction on the grammar.
5. Recursion depth = tree height on both sides — 10^4 on the chain test, past stock CPython's ~1000 default (fine under this judge's raised limit). The interview-complete remark: either raise the limit, or switch to the BFS/level-order codec, whose loop-based encode/decode is naturally iterative — the "per-level BFS vs per-subtree DFS" trade-off again, chosen here by robustness rather than by output shape.
6. Empty tree falls out for free: `serialize(None)` = `"#"`, which decodes to `None`.

## 5. Annotated Python solution

```python
class Codec:
    def serialize(self, root) -> str:
        parts = []

        def dfs(node):
            if not node:
                parts.append("#")   # explicit null: makes decoding forced
                return
            parts.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(parts)      # join once; += in the loop is O(n^2)

    def deserialize(self, data: str):
        tokens = iter(data.split(","))

        def build():
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()     # consumes exactly the left subtree
            node.right = build()    # iterator now sits at the right subtree
            return node

        return build()
```

## 6. Complexity

- **Time O(n)** both directions — "each node and each null slot produces or consumes exactly one token."
- **Space O(n)** for the string, **O(h)** recursion — "the string stores n values plus n+1 markers; the stack is bounded by height."

## 7. Edge-case traps

- **Empty tree** → `"#"` → `None`; forgetting this crashes on the visible test.
- **Negative values** — any format that detects nulls by "token isn't a digit" breaks on `-7`; compare against the marker, don't `isdigit()`.
- **Duplicate values** — sinks preorder+inorder reconstruction; structure must come from markers, not value identity.
- **Deep chains** — recursion depth on both encode and decode; also the 2^h blowup for naive full-array level-order.
- **String concatenation in the loop** — quadratic; accumulate in a list.
- **Delimiter-free formats** — multi-digit and negative numbers make `"12"` vs `"1","2"` ambiguous; always join with a separator.

## 8. (DP section — not applicable)

Not DP. Template trained: **self-delimiting preorder with null markers + shared-iterator recursive descent** — the same consume-as-you-recurse move that parses nested expressions and rebuilds trees from any marker-annotated traversal.

## 9. Interviewer follow-up

- *"Make the string shorter for a BST"* — Serialize BST 449: markers become unnecessary; preorder values alone suffice because BST bounds (the pass-constraints-down trick from Validate BST 98) tell the decoder where subtrees end. Nice callback: constraints replace markers.
- *"Binary instead of text?"* — length-prefixed varints or fixed-width ints; nulls become a bitmap; discuss endianness and versioning.
- *"n-ary tree?"* — child count after each value, or a sentinel closing each child list (LC 428).
- *"Streams too deep to recurse?"* — iterative preorder with an explicit stack for encode; for decode, a stack of "nodes awaiting children" — or switch wholesale to the level-order codec.
