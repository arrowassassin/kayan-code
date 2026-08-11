## Hint 1

You need two things at once: O(1) lookup by key, and O(1) access to "the least recently used" plus O(1) reordering on every use. No single built-in structure gives you both — think about combining two.

## Hint 2

A hash map gives O(1) lookup. For the recency order, you need a sequence where you can (a) remove a node from the middle in O(1) and (b) append to one end in O(1). Which linked structure supports middle removal in O(1) *if you already hold a reference to the node*?

## Hint 3

Map keys to **doubly-linked-list nodes**. On every get/put, unlink the node and re-insert it at the "most recent" end; evict from the other end. Use two sentinel nodes (dummy head and tail) so you never special-case empty/one-element lists. (In an interview, mention `OrderedDict.move_to_end` as the pragmatic Python shortcut — then show you can build it raw.)
