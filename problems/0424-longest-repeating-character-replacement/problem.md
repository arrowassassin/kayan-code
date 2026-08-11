# Longest Repeating Character Replacement

You are given a string `s` of uppercase English letters and an integer `k`. You may pick at most `k` positions in `s` and overwrite each with any uppercase letter you like.

Return the length of the longest contiguous substring consisting of a **single repeated letter** that you can produce this way.

## Example 1

```
Input: s = "ABAB", k = 2
Output: 4
```

Replace both `'A'`s (or both `'B'`s) and the whole string becomes one letter.

## Example 2

```
Input: s = "AABABBA", k = 1
Output: 4
```

Replace the middle `'A'` in `"ABBA"` to get `"AABBBBA"` — the run `"BBBB"` has length 4.

## Constraints

- `1 <= len(s) <= 10^5`
- `s` consists of uppercase English letters only
- `0 <= k <= len(s)`

With `k = 0` the answer is simply the longest existing run of one letter.
