## Hint 1

Every path in a tree has a unique **highest** node where it bends — its two ends hang down from there. What do you know about the two halves of the path below that bend?

## Hint 2

Seen from its bend node, the path is (longest drop into the left subtree) + (longest drop into the right subtree) + the two connecting edges. "Longest drop" is just subtree height — a quantity a post-order traversal can return upward.

## Hint 3

Write one recursive function that returns the height (in edges) of each subtree, and as a side effect updates a global best with `left_height + right_height + 2` at every node. Use height `-1` for the empty subtree so leaves come out as height `0` and the arithmetic needs no special cases.
