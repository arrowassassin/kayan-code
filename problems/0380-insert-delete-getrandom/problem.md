# Insert Delete GetRandom O(1)

Design a set of integers where insertion, deletion, and drawing a uniformly random member all run in **O(1) average time**. Implement `RandomizedSet`:

- `RandomizedSet()` — create an empty set.
- `insert(val) -> bool` — add `val`; return `True` if it was not already present, `False` otherwise (no duplicates are ever stored).
- `remove(val) -> bool` — delete `val`; return `True` if it was present, `False` otherwise.
- `getRandom() -> int` — return one element chosen uniformly at random from the current members. It is only called when the set is non-empty.

Each element currently in the set must be returned by `getRandom` with equal probability.

## Example

```
RandomizedSet s = RandomizedSet()
s.insert(1)      # True
s.remove(2)      # False  (not present)
s.insert(2)      # True   set: {1, 2}
s.getRandom()    # 1 or 2, each with probability 1/2
s.remove(1)      # True   set: {2}
s.insert(2)      # False  (already present)
s.getRandom()    # 2      (only member)
```

## Constraints

- `-2^31 <= val <= 2^31 - 1`
- Up to `2 * 10^5` total calls to `insert`, `remove`, and `getRandom`
- `getRandom` is never called on an empty set
