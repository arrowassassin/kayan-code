## Hint 1

Don't look for one clever traversal that produces the whole answer. The boundary is defined as four separate pieces — treat it as four small, independent problems glued together in order.

## Hint 2

The only real difficulty is double-counting. Decide up front which pass *owns* each node: the root belongs to the root pass alone, leaves belong to the leaf pass alone, and the two side walks must therefore skip every leaf they touch — including the bottom node of their own path.

## Hint 3

Left boundary: walk down from `root.left`, preferring `left` and falling back to `right`, appending non-leaf values. Leaves: one plain DFS appending leaf values left-to-right (skip the root). Right boundary: mirror walk from `root.right` preferring `right`, but push onto a stack and emit it reversed. Handle the single-node tree before any of the three passes run.
