# Insert Delete GetRandom O(1) — Editorial

## 1. Pattern recognition

"Design a class, three operations, each O(1) average" — like its warmup LRU Cache, this is the **composite data structure** pattern: list the primitive each requirement demands, notice no single structure supplies all of them, and fuse two while keeping them consistent. The new wrinkle is `getRandom`: *uniform* selection in O(1) is only possible over **contiguously indexed** storage, and that one word — uniform — dictates the entire design. State the per-op budget for all three methods before coding; that framing is what the interviewer scores.

## 2. Brute force first

A Python `set` alone: insert/remove O(1), but `getRandom` must materialize an iteration — `random.choice(tuple(s))` is O(n) per call. A sorted list or `list`+`index()`: random is O(1) but remove costs an O(n) scan/shift. Either way, 2×10⁵ operations at O(n) each is up to ~2×10¹⁰ element touches on adversarial patterns — hopeless, and more decisively, the statement *names* O(1) per op, so an interviewer stops you at the requirement before any benchmark does.

## 3. The key insight

**A set has no meaningful order — so removal may freely swap the victim with the array's last element, turning "delete from the middle" into "pop from the end", both O(1).**

## 4. Step-by-step derivation

1. `getRandom` uniform in O(1) ⇒ elements must live in an array: draw `randrange(len)` and index. Any hole in the array skews the distribution or forces re-draws.
2. `insert`/`remove` in O(1) ⇒ a dict for membership. But remove must also fix the array, and array middle-deletion is O(n) — the shift preserves order we don't need.
3. Exploit the freedom: overwrite slot `i` (the victim) with the last element, then pop the tail. The array stays dense; only ONE surviving element changed position — so the dict needs exactly one index update: `pos[last] = i`. This is why the dict maps **value → index** and not just membership: remove must locate the victim's slot without searching.
4. Order of operations matters when the victim *is* the last element: write `pos[last] = i` first and `del pos[val]` last, and the self-swap degenerates into a harmless no-op instead of resurrecting the deleted key.
5. Amortized honesty: `list.append`/`pop` are amortized O(1) — occasional resizes copy the array, but each element pays for its own future copy. Say "average/amortized O(1)", and note dict operations are also average-case (hash collisions are the worst case).

## 5. Annotated Python solution

```python
import random


class RandomizedSet:
    def __init__(self):
        self.vals = []      # dense array -> uniform getRandom by index
        self.pos = {}       # val -> index in vals; membership AND locator

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)
        self.vals.append(val)               # amortized O(1)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.vals[-1]
        self.vals[i] = last                 # fill the hole with the tail
        self.pos[last] = i                  # the ONE index that moved
        self.vals.pop()                     # shrink; order was never sacred
        del self.pos[val]                   # AFTER pos[last]: safe when val == last
        return True

    def getRandom(self) -> int:
        return self.vals[random.randrange(len(self.vals))]
```

## 6. Complexity

- **Time O(1)** average per operation — "insert and remove are a constant number of dict and tail-of-array touches; getRandom is one random draw and one index."
- **Space O(n)** — "one array slot plus one dict entry per current member."

## 7. Edge-case traps

- **Removing the last element itself** — the swap is a self-swap; with the wrong update order (`del` before `pos[last] = i`) the key gets re-inserted and the set is silently corrupted. This is *the* bug of this problem.
- **Insert of an existing value must return `False` and change nothing** — including not touching the array.
- **Remove → insert → remove of the same value** — cycles stress stale indices; every swap must update `pos` or a later remove hits the wrong slot.
- **Single-element set** — `getRandom` must return that element; `randrange(1)` is fine, `randint(0, len-1)` off-by-ones are not.
- **Uniformity** — drawing from the dict's keys or iterating "a few" elements is not uniform-in-O(1); the dense array is the only honest source.

## 8. (DP section — not applicable)

Not DP. The reusable template: **swap-with-last deletion over a dense array + value→index map** — the standard trick for O(1) delete wherever order is irrelevant (it also powers heap element removal and entity-slot allocators).

## 9. Interviewer follow-up

- *"Allow duplicates (RandomizedCollection 381)"* — `pos` becomes value → *set of indices*; on remove, pick any index of the victim, swap the tail in, and update the tail's index set (delicately: the tail may be another copy of the same value). Uniformity now weights values by multiplicity, which the array gives for free.
- *"getRandom weighted by insertion recency?"* — you now care about order, so the swap trick dies; discuss a Fenwick tree over weights: O(log n) ops, sampling by prefix-sum search.
- *"Thread safety at scale?"* — remove mutates array and dict in a multi-step sequence with a mid-state where they disagree; readers of `getRandom` can see a torn view, so a lock (or sharding the value space and locking per shard) is required — contrast with LRU Cache, where the shared recency list makes sharding much harder.
- *"Persist to disk / distribute?"* — the array-index coupling is memory-local; a distributed uniform-random-member service instead samples a random shard weighted by shard size, then samples within — the same two-level uniformity argument, one level up.
