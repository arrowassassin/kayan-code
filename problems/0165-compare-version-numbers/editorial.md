# Compare Version Numbers — Editorial

## 1. Pattern recognition

Dot-delimited fields with per-field numeric meaning: this is **tokenize, normalize, compare component-wise** — the same shape as comparing dates, IP addresses, or dotted database schema versions. The two spec sentences that matter are the normalization rules: leading zeros don't count, and missing chunks are zeros. Read the spec aloud and enumerate what a token *is* (a decimal integer, possibly zero-padded) and what "absent" means (zero) — both rules are traps for anyone comparing text instead of values. The instinct this problem drills: the moment a comparison has *semantic* rules attached, stop comparing characters.

## 2. Brute force first

The naive answer — plain string comparison, maybe after padding to equal length — fails immediately: `"1.2" < "1.10"` is false lexicographically because `'2' > '1'` character-wise, and `"1.0" == "1"` is false textually but true semantically. A subtler half-measure is stripping leading zeros textually and comparing chunk strings — but then `"10"` vs `"9"` still compares wrong (`'1' < '9'`) unless you *also* compare lengths first. Every textual patch is another rule reimplemented by hand; converting to integers implements all of them at once. That's the parse-don't-patch lesson.

## 3. The key insight

**Split on dots, convert each chunk with `int()` (which erases leading zeros), treat a missing chunk as 0, and return at the first unequal pair.**

## 4. Step-by-step derivation

1. `version.split(".")` yields the chunks; the constraints promise no empty chunks (no leading/trailing/double dots), so every piece is a valid digit string.
2. `int(chunk)` is the whole normalization step: `"01"`, `"001"`, `"1"` all become 1. In an interview, note you *could* parse digits manually (`v = v*10 + d`) — worth saying to show you know what `int()` does — but the library call is the correct pragmatic choice, not a shortcut.
3. Unequal lengths: conceptually pad the shorter list with zeros. Implement by looping to `max(len(a), len(b))` and substituting 0 out of range — no actual padding allocation, no tail special-case. This is why `"1.0.0.0"` equals `"1"` without any code mentioning it.
4. Compare left to right and **return immediately** on the first difference — later chunks are irrelevant once an earlier one differs (`"7.5.2.4"` vs `"7.5.3"` is decided at chunk 2 despite v1 being "longer").
5. Fall out of the loop → all chunks equal (including padded zeros) → return 0.

## 5. Annotated Python solution

```python
class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        a = version1.split(".")
        b = version2.split(".")
        for i in range(max(len(a), len(b))):
            # missing chunks count as 0, and int() eats leading zeros
            x = int(a[i]) if i < len(a) else 0
            y = int(b[i]) if i < len(b) else 0
            if x != y:
                return -1 if x < y else 1
        return 0
```

## 6. Complexity

- **Time O(n + m)** — "split touches each character once, and each chunk is converted to an integer exactly once."
- **Space O(n + m)** — "the two chunk lists; O(1) if you walk the strings with indices instead of splitting."

## 7. Edge-case traps

- **Leading zeros** (`"1.01"` vs `"1.001"` → 0, `"00.00"` vs `"0.0.0"` → 0) — textual comparison dies here.
- **Unequal chunk counts both ways** (`"1.0.1"` vs `"1"` → 1, `"2"` vs `"2.0.0.1"` → -1) — the padding must be symmetric.
- **Trailing zero chunks** (`"1.0.0.0.0"` vs `"1"` → 0) — equality despite very different lengths.
- **Multi-digit chunks** (`"1.2"` vs `"1.10"` → -1, `"10.4"` vs `"9.9"` → 1) — the classic lexicographic trap.
- **Return exactly −1/0/1** — not "any negative number"; the spec is a three-valued result, not a comparator contract.
- **32-bit-boundary chunks** (`"2147483647"`) — fine in Python; in fixed-width languages, mention overflow before the interviewer does.

## 8. (DP section — not applicable)

Not DP. This trains the **split → normalize → component-wise compare** template with zero-padding by substitution — reusable for dates, IPs, semver, and any dotted-hierarchy ordering.

## 9. Interviewer follow-up

- *"Support pre-release tags like `1.0.0-beta.2` (semver)"* — now chunks are mixed-type: numeric identifiers compare numerically, alphanumeric ones lexically, and a pre-release sorts *before* the release. The token-class enumeration habit is exactly what keeps this extension manageable.
- *"O(1) extra space"* — walk both strings with index pointers, parsing each chunk in place (accumulate until `'.'`); same logic, no lists — this is the manual-parse version made useful.
- *"Sort a million version strings"* — don't compare pairwise from scratch: precompute each version's chunk tuple once (decorate–sort–undecorate); note tuples of unequal length need explicit zero-padding to the max width, or trailing zeros will make `(1,)` sort before `(1, 0)` — which happens to be equal here, a nice subtlety to raise yourself.
- *"What if chunks can be huge (hundreds of digits)?"* — Python big ints absorb it; elsewhere compare stripped digit strings by (length, lexicographic) — the textual method done *right*.
