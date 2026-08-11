# Longest Palindromic Substring

Given a string `s`, return the longest **contiguous** substring of `s` that reads the same forwards and backwards.

If several palindromic substrings tie for the maximum length, returning **any one of them** is accepted.

## Example 1

```
Input: s = "babad"
Output: "bab"
```

`"aba"` is equally valid — both have length 3.

## Example 2

```
Input: s = "cbbd"
Output: "bb"
```

The longest palindrome here has even length — don't forget those.

## Example 3

```
Input: s = "ac"
Output: "a"
```

`"c"` is equally valid: every single character is a palindrome of length 1.

## Constraints

- `1 <= len(s) <= 1000`
- `s` consists of digits and English letters (case-sensitive: `"Aa"` is not a palindrome)

Substring means contiguous — this is not the subsequence problem.
