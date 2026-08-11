## Hint 1

A preorder listing of values alone cannot be inverted — many trees share it. What minimal extra information makes one traversal order uniquely decodable?

## Hint 2

Record the nulls. Preorder with an explicit marker for every empty child (say `#`) makes the string self-describing: the decoder always knows whether the next token starts a subtree or ends one. Think about why you then need no bracket structure and no second traversal.

## Hint 3

`serialize`: preorder DFS appending `str(val)` or `#`, joined with commas (join once at the end — repeated string `+=` is quadratic). `deserialize`: wrap the token list in an iterator; a recursive `build()` consumes one token, returns `None` on `#`, otherwise makes the node and calls itself for left then right. The iterator's shared position is what stitches the subtrees together. A BFS/level-order encoding works too and dodges deep recursion.
