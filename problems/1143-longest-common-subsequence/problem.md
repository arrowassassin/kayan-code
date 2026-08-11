# Longest Common Subsequence

Given two strings `text1` and `text2`, return the length of their longest **common subsequence** — the longest string that can be obtained from *both* inputs by deleting characters (keeping the remaining characters in their original order).

If the strings share no characters at all, the answer is `0`.

## Example 1

```
Input: text1 = "abcde", text2 = "ace"
Output: 3
```

`"ace"` appears in order inside both strings.

## Example 2

```
Input: text1 = "abc", text2 = "def"
Output: 0
```

No common characters.

## Example 3

```
Input: text1 = "bsbininm", text2 = "jmjkbkjkv"
Output: 1
```

Only a single character (`"b"` — or `"m"`) can be aligned.

## Constraints

- `1 <= len(text1), len(text2) <= 1000`
- Both strings consist of lowercase English letters only

A subsequence need not be contiguous — that is what separates this from longest common *substring*.
