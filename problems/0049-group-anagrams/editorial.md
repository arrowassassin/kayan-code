# Group Anagrams — Editorial

## 1. Pattern recognition

"Partition items into equivalence classes" is the **canonical-key hashing** pattern: don't compare items to each other, compare each item to a normal form. The equivalence here — same letters, any order — is the character-multiset relation, so the normal form must erase order while preserving multiplicity. The classic interview "duplicate/character analysis" family lives exactly here: the interview skill being probed is *choosing the canonicalization*, and saying clearly why it's sound (equal keys ⇔ anagrams, both directions).

## 2. Brute force first

For each string, scan all existing groups and test anagram-ness against a representative (compare sorted copies or histograms): O(n · g · L) with g groups — in the worst case (all singletons) that's O(n² L), i.e. ~10⁸ character operations at n = 10⁴. It also re-answers the same question ("are these two equivalent?") over and over. The fix is the standard one: make equivalence checkable by *equality of a key*, then a hash map answers membership in O(1) — pairwise comparison becomes bucket insertion.

## 3. The key insight

**Map every string to a canonical key that is invariant under letter rearrangement — its sorted form or its letter histogram — and let `dict[key].append(s)` do the grouping.**

## 4. Step-by-step derivation

1. Define the equivalence precisely: `a ~ b` iff the multiset of letters matches. Any injective function *of the multiset* is a valid key.
2. Candidate 1: `''.join(sorted(s))`. Sound because sorting is a canonical ordering of the multiset. Cost O(L log L) per string. Simple, idiomatic, the usual interview answer.
3. Candidate 2: a 26-slot count array, converted to a `tuple` so it's hashable. Sound because a multiset *is* its count vector. Cost O(L + 26) per string — asymptotically better, and the better answer when L is large or the alphabet is fixed. Mentioning both, with the trade-off, is the expected move.
4. One pass: `groups[key].append(s)` with a `defaultdict(list)`; emit `list(groups.values())`. Duplicates naturally land twice in the same bucket; the empty string's key (empty sorted string / all-zero tuple) is as valid as any other — no special cases anywhere.
5. Don't stringify the histogram by naive concatenation (`"1" + "11"` vs `"11" + "1"` collide); the tuple avoids the delimiter bug entirely. If you must build a string key, join with a separator.

## 5. Annotated Python solution

```python
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = defaultdict(list)
        for s in strs:
            counts = [0] * 26                    # letter histogram: O(L) per word
            for ch in s:
                counts[ord(ch) - 97] += 1
            groups[tuple(counts)].append(s)      # tuple -> hashable canonical key
        return list(groups.values())
```

## 6. Complexity

- **Time O(n · L)** — "each string is scanned once to build its histogram; hashing the 26-tuple is constant."
- **Space O(n · L)** — "every input string is stored in exactly one bucket, plus one 26-tuple per distinct class."

## 7. Edge-case traps

- **Empty string** — must form a normal group; code that indexes `s[0]` or skips empty keys breaks.
- **Exact duplicates** (`["dog","god","dog"]`) — both occurrences of `"dog"` belong in one group; dedup-by-set solutions lose one.
- **All strings one group / all singletons** — the two extremes of bucket shape; the singleton case is what kills the O(n²) brute force.
- **Histogram-as-string keys without delimiters** — count vectors like (1,11) vs (11,1) can collide when concatenated; use a tuple.
- **Single-character strings** and 1-element input — trivial but worth a glance at the return shape: a list of lists, never a flat list.

## 8. (DP section — not applicable)

Not DP. This trains the **canonicalize-then-hash** template — the same normal-form trick behind Valid Anagram, Isomorphic Strings (structural encoding), and dedup keys in data pipelines.

## 9. Interviewer follow-up

- *"Unicode input?"* — the fixed 26-slot array dies; use a `Counter` frozen as `frozenset(counter.items())` or fall back to the sorted-string key. The point: histogram keys assume a bounded alphabet.
- *"Streaming / too big for memory"* — the key doubles as a shard key: map each string to `hash(canonical)` mod k workers, group locally, no cross-shard merging needed since classes never span shards. This problem is the in-memory kernel of a shuffle.
- *"Group only strings that are one edit apart"* — no longer an equivalence relation (not transitive), so the key trick fails; that contrast is worth articulating.
- *"Return groups sorted by size"* — trivial post-sort; note the judge here accepts any order, which is what `unordered_2d`-style comparison means.
