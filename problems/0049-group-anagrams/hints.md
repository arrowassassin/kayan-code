## Hint 1

"Bundle equivalent items together" is a hashing problem in disguise: if you can compute a **canonical key** that is identical for exactly the strings that belong together, a dictionary from key to list does all the grouping.

## Hint 2

What is invariant under rearranging letters? Two candidates: the letters in sorted order, and the count of each letter. Either works as a key — think about what each costs per string and which one is hashable in Python.

## Hint 3

Use a `dict` mapping key → list of originals. Sorted-string key: `''.join(sorted(s))`, O(L log L) per string. Count key: a 26-slot histogram turned into a `tuple` (lists aren't hashable), O(L) per string. Return `list(groups.values())` — and make sure the empty string and duplicate strings flow through without special cases.
