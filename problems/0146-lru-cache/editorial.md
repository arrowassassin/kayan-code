# LRU Cache — Editorial

## 1. Pattern recognition

"Design a class", "O(1) per operation", "evict by recency" — this is the **composite data structure** design pattern: no single structure meets all the requirements, so you glue two together and keep them in sync. The Snowflake angle: their reported "stream-processing class design" questions are exactly this family — state machines with strict per-op complexity budgets.

## 2. Brute force first

Keep a dict plus a Python list ordering keys by recency. `get`/`put` then need `list.remove(key)` — O(n) per operation, O(n·q) overall. With 10⁵ operations over 3,000 keys that's up to ~3×10⁸ list shifts: too slow, and more importantly it violates the *stated* O(1) requirement — an interviewer will stop you at the requirement, not the benchmark.

## 3. The key insight

**A hash map can point directly at linked-list nodes, and a doubly linked list can unlink a node in O(1) once you hold it — together they make "find + reorder" constant time.**

## 4. Step-by-step derivation

1. Requirement A: O(1) key lookup → hash map, non-negotiable.
2. Requirement B: O(1) "move this entry to most-recent" and O(1) "pop least-recent". An array can't (middle removal shifts); a singly linked list can't (removal needs the *previous* node); a **doubly** linked list can — if you can reach the node without searching.
3. Fuse them: `map[key] -> node`, nodes chained in recency order. Every `get`/`put` unlinks the touched node and pushes it to the front; eviction pops from the back.
4. Kill the edge cases structurally: two **sentinel** nodes (dummy head + tail) mean the list is never empty and no operation ever checks for None neighbors.
5. Each operation is a dict access plus a constant number of pointer swaps → O(1).

## 5. Annotated Python solution

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")   # key stored so eviction can clean the map

    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}
        self.head = Node()              # sentinels: never empty, no None checks
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)              # touch = move to most-recent end
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:             # update path: no eviction ever
            node = self.map[key]
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:   # evict BEFORE inserting
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]       # this is why nodes store their key
        node = Node(key, value)
        self.map[key] = node
        self._push_front(node)
```

## 6. Complexity

- **Time O(1)** per `get`/`put` — "one dict lookup plus a constant number of pointer updates."
- **Space O(capacity)** — "one map entry and one list node per cached key."

## 7. Edge-case traps

- **`put` on an existing key at full capacity** must *not* evict — it's an update, size doesn't grow. This is the classic bug.
- **Capacity 1** — every new put evicts; get-then-put sequences stress the pointer logic.
- **`get` on a missing key must not disturb recency** of anything.
- **Update must move the key to most-recent**, not just change the value.
- Forgetting to store the **key inside the node** makes eviction unable to delete from the map.

## 8. (DP section — not applicable)

Not DP. The reusable skill: sentinel-guarded doubly linked list + map — the same fusion powers LFU Cache and many "O(1) design" questions.

## 9. Interviewer follow-up

- *"Make it thread-safe"* — one lock around each operation is the honest baseline; discuss why per-bucket locking on the map doesn't compose with the shared recency list.
- *"Add TTL expiry"* — store an expiry timestamp per node; lazily evict on access, and mention a background sweep or a min-heap of expirations for proactive cleanup.
- *"LFU instead of LRU?"* — frequency buckets, each bucket its own recency list, plus a min-frequency pointer (LFU Cache 460) — same building blocks, one more level.
- The pragmatic-Python remark — "in production I'd reach for `functools.lru_cache` or `OrderedDict.move_to_end`" — scores points *after* you've shown the raw structure.
