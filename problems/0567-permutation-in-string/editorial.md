# Permutation in String — Editorial

## 1. Pattern recognition

Two words in the statement do all the work: a permutation of `s1` inside `s2` must be *contiguous* and must have length *exactly* `len(s1)`. That collapses the search space from "all substrings" to "all windows of one fixed size" — the **fixed-size sliding window**, the simplest member of the family. Where variable-size windows (Longest Substring, Minimum Window) juggle when to shrink, a fixed window slides in lockstep: one character enters, one leaves, every step. The remaining question is purely "how cheaply can I compare the window's contents against a target multiset?"

## 2. Brute force first

For each of the O(n₂) starting positions, sort the length-n₁ slice and compare with sorted `s1`: O(n₂ · n₁ log n₁). With both lengths at 10⁴ that's ~10⁹ operations — over budget, and it recomputes from scratch information that changes by exactly two characters per slide. Even the counting version done naively — rebuild a `Counter` per window — is O(26 · n₁ · n₂)-ish. The fix in both cases is the same: never rebuild what you can update.

## 3. The key insight

**A window is a permutation of `s1` iff their 26-letter count vectors are equal — and one slide changes only two of those 26 counts.**

## 4. Step-by-step derivation

1. Anagram test = count-vector equality. Build `need` (counts of `s1`) once, and `win` (counts of the first n₁ characters of `s2`).
2. Slide: `win[entering] += 1`, `win[leaving] -= 1`. Comparing `win == need` per slide is O(26) — total O(26 · n₂). That already passes comfortably and is a fine first answer; say its complexity out loud before optimizing.
3. To make each slide O(1), track `matches`: how many of the 26 letters currently have `win[i] == need[i]`. When a count changes by 1 it can only cross into agreement (`win[i]` becomes `need[i]`: `matches += 1`) or out of it (`win[i]` was `need[i]`, now off by one: `matches -= 1`). Two changed letters → at most four adjustments.
4. Answer `True` the moment `matches == 26`; check once after building the initial window too — the match might be at position 0, and a loop that only checks after the first slide silently misses it.
5. Guard `len(s1) > len(s2)` before building windows, or the initial fill reads past the string.

## 5. Annotated Python solution

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)
        if n1 > n2:
            return False

        need, win = [0] * 26, [0] * 26
        a = ord("a")
        for i in range(n1):
            need[ord(s1[i]) - a] += 1
            win[ord(s2[i]) - a] += 1

        matches = sum(1 for i in range(26) if need[i] == win[i])
        if matches == 26:              # match may sit at index 0
            return True

        for right in range(n1, n2):
            i = ord(s2[right]) - a     # entering char
            win[i] += 1
            if win[i] == need[i]:
                matches += 1
            elif win[i] == need[i] + 1:  # was equal, just overshot
                matches -= 1
            j = ord(s2[right - n1]) - a  # leaving char: window size stays n1
            win[j] -= 1
            if win[j] == need[j]:
                matches += 1
            elif win[j] == need[j] - 1:  # was equal, just undershot
                matches -= 1
            if matches == 26:
                return True
        return False
```

## 6. Complexity

- **Time O(n₁ + n₂)** — "one pass to build counts, one slide per remaining character, constant work per slide."
- **Space O(1)** — "two 26-slot arrays, independent of input size."

## 7. Edge-case traps

- **`len(s1) > len(s2)`** → `False` before touching any window.
- **Match at position 0** — the pre-loop `matches == 26` check; omitting it is the classic off-by-one here.
- **Repeated letters in `s1`** (`"abcabc"`) — set-based membership tests give false positives; only full counts work.
- **All needed letters present but never adjacent** (`"abc"` vs `"ccccbbbbaaaa"`) → `False`; frequency of letters in all of `s2` proves nothing.
- **`s1` of length 1** — reduces to `s1[0] in s2`; the general code must still get it right.

## 8. Reusable template

Not DP. This trains the fixed-size window with count matching — enter/leave symmetry plus the `matches` counter — the identical machinery behind Find All Anagrams in a String (438), which differs only in collecting every index instead of returning at the first.

## 9. Interviewer follow-up

- *"Return **all** starting indices, not just existence"* — that's literally Find All Anagrams (438): same loop, append `right - n1 + 1` whenever `matches == 26` instead of returning.
- *"Unicode instead of lowercase?"* — swap arrays for hash maps and track `mismatched_keys` (count of letters where the maps disagree) reaching 0; the O(1)-per-slide structure survives, the fixed 26 does not.
- *"Allow up to k mismatched characters"* — the window is valid when at most k positions' worth of counts disagree; maintain the total absolute count difference instead of per-letter equality — a nice bridge toward budgeted windows like Character Replacement (424).
