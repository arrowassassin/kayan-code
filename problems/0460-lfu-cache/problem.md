# LFU Cache

Design a fixed-capacity key–value cache that evicts the **least frequently used** entry when full. Implement the class `LFUCache`:

- `LFUCache(capacity)` — initialize with the given capacity (which may be `0`).
- `get(key) -> int` — return the value stored at `key`, or `-1` if absent. A successful `get` increments the key's **use counter**.
- `put(key, value)` — insert or update `key`. Updating an existing key also increments its use counter. If inserting a **new** key would exceed capacity, first evict the key with the **smallest use counter**; if several keys are tied for the smallest counter, evict the **least recently used** among them.

A key's use counter starts at `1` when it is inserted (the insert itself counts as a use) and resets if the key is ever evicted and inserted again.

Both operations must run in **O(1) average time**.

## Example

```
LFUCache cache = LFUCache(2)
cache.put(1, 1)        # counters: {1: 1}
cache.put(2, 2)        # counters: {1: 1, 2: 1}
cache.get(1)           # returns 1;  counters: {1: 2, 2: 1}
cache.put(3, 3)        # evicts key 2 (counter 1 < 2)
cache.get(2)           # returns -1
cache.get(3)           # returns 3;  counters: {1: 2, 3: 2}
cache.put(4, 4)        # tie at counter 2 -> evicts key 1 (least recently used)
cache.get(1)           # returns -1
cache.get(3)           # returns 3
cache.get(4)           # returns 4
```

## Constraints

- `0 <= capacity <= 10^4`
- `0 <= key, value <= 10^5`
- Up to `2 * 10^5` calls to `get` and `put`
- With `capacity = 0`, every `put` is a no-op and every `get` returns `-1`
