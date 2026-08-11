## Hint 1

A hash set gives O(1) insert and remove, but drawing a *uniform* random member in O(1) needs indexable storage — `random.choice` over a set isn't O(1). A plain list gives O(1) random access, but O(n) membership and removal. Neither alone suffices; this is a two-structure fusion like LRU Cache.

## Hint 2

Keep the members in a dynamic array (uniform random = one `randrange` index) *and* a dict mapping each value to its array index. Insert appends. The hard part is remove: deleting from the middle of an array is O(n) — unless you notice the array's order doesn't matter at all.

## Hint 3

To remove the element at index `i`: copy the **last** element into slot `i`, update that element's index in the dict, then pop the tail and delete the victim's dict entry. Constant work, no hole. Walk through removing the last element itself to make sure your update order doesn't corrupt the dict.
