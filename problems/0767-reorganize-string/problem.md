# Reorganize String

Given a string `s` of lowercase letters, rearrange its characters so that **no two neighboring characters are equal**, and return the rearranged string. If no such arrangement exists, return the empty string `""`.

Any valid rearrangement is accepted — there is usually more than one.

## Example 1

```
Input: s = "aab"
Output: "aba"
```

`"aba"` uses the same letters with the two `a`s separated. (`"aab"` itself is invalid — the `a`s touch.)

## Example 2

```
Input: s = "aaab"
Output: ""
```

Three `a`s need at least two separators, but only one `b` exists — impossible.

## Constraints

- `1 <= len(s) <= 10^5`
- `s` consists of lowercase English letters only
- Your returned string must be a permutation of `s` (or exactly `""` when impossible)
