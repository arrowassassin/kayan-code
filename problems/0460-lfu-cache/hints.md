## Hint 1

You solved LRU with a map pointing into one recency-ordered list. Here the primary eviction key is the use *counter*, with recency only as a tie-break. One ordered list can't encode both — think about keeping one recency structure **per counter value**.

## Hint 2

Group keys into frequency buckets: `buckets[f]` holds every key whose counter is `f`, in recency order. Eviction always pops the oldest key from the bucket of the **smallest** occupied frequency. The remaining puzzle: how do you know the smallest occupied frequency in O(1) without scanning?

## Hint 3

Track a single `min_freq` integer. It only ever changes two ways: any brand-new insert sets `min_freq = 1` (a new key has counter 1, the global minimum), and when a get/put drains the bucket at `min_freq`, that key moved to `f + 1`, so `min_freq` becomes `f + 1`. In Python, an `OrderedDict` per bucket gives you O(1) "remove this key" and O(1) "pop oldest" — the same roles the doubly linked list played in LRU.
