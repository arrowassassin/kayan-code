# Permutation in String

Given two lowercase strings `s1` and `s2`, decide whether `s2` contains a contiguous substring that is a **rearrangement** (permutation) of `s1`. Return `True` if such a substring exists, otherwise `False`.

Equivalently: is there a window of `s2` of length `len(s1)` with exactly the same letter counts as `s1`?

## Example 1

```
Input: s1 = "ab", s2 = "eidbaooo"
Output: true
```

The substring `"ba"` is a rearrangement of `"ab"`.

## Example 2

```
Input: s1 = "ab", s2 = "eidboaoo"
Output: false
```

`'b'` and `'a'` appear in `s2` but never adjacently in either order.

## Constraints

- `1 <= len(s1), len(s2) <= 10^4`
- `s1` and `s2` consist of lowercase English letters only

If `len(s1) > len(s2)`, the answer is `False`.
