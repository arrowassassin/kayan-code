# LRU Cache

Design a fixed-capacity key–value cache that evicts the **least recently used** entry when full. Implement the class `LRUCache`:

- `LRUCache(capacity)` — initialize with a positive capacity.
- `get(key) -> int` — return the value stored at `key`, or `-1` if absent. A successful `get` counts as a *use*.
- `put(key, value)` — insert or update `key`. Updating counts as a *use*. If inserting a **new** key would exceed capacity, first evict the least recently used key.

Both operations must run in **O(1) average time**.

## Example

```
LRUCache cache = LRUCache(2)
cache.put(1, 1)        # cache: {1=1}
cache.put(2, 2)        # cache: {1=1, 2=2}
cache.get(1)           # returns 1, 1 is now most recent
cache.put(3, 3)        # evicts key 2 (least recent)
cache.get(2)           # returns -1
cache.put(4, 4)        # evicts key 1
cache.get(1)           # returns -1
cache.get(3)           # returns 3
cache.get(4)           # returns 4
```

## Constraints

- `1 <= capacity <= 3000`
- `0 <= key, value <= 10^4`
- Up to `10^5` calls to `get` and `put`
