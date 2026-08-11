# Longest Substring Without Repeating Characters

Given a string `s`, find the length of the longest **contiguous** substring in which no character appears more than once, and return that length.

Note that we're asking about substrings (contiguous runs), not subsequences — `"pwke"` is a subsequence of `"pwwkew"`, not a substring.

## Example 1

```
Input: s = "abcabcbb"
Output: 3
```

The longest run with all-distinct characters is `"abc"`, length 3.

## Example 2

```
Input: s = "bbbbb"
Output: 1
```

Every character is the same, so no valid substring is longer than a single `"b"`.

## Example 3

```
Input: s = "pwwkew"
Output: 3
```

`"wke"` (or `"kew"`) has length 3.

## Constraints

- `0 <= len(s) <= 5 * 10^4`
- `s` consists of English letters, digits, symbols and spaces

An empty string has answer `0`.
