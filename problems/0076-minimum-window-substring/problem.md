# Minimum Window Substring

You are given two strings `s` and `t`. Return the **shortest** contiguous substring of `s` that contains every character of `t`, *counting multiplicity* — if `t` contains two `'C'`s, the window must contain at least two `'C'`s. If no such window exists, return the empty string `""`.

The test data guarantees that when a valid window exists, the shortest one is **unique**.

## Example 1

```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

`"BANC"` contains `'A'`, `'B'` and `'C'`; no shorter substring of `s` does.

## Example 2

```
Input: s = "a", t = "a"
Output: "a"
```

## Example 3

```
Input: s = "a", t = "aa"
Output: ""
```

`t` needs two `'a'`s but `s` only has one, so no window qualifies.

## Constraints

- `1 <= len(s), len(t) <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters
- Uppercase and lowercase are **distinct** characters

Aim for a solution that runs in `O(len(s) + len(t))`.
