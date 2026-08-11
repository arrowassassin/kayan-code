# Decode Ways

A message of capital letters was encoded by replacing each letter with its alphabet position: `'A' -> "1"`, `'B' -> "2"`, ..., `'Z' -> "26"`, and the digits were concatenated with no separators.

Given the resulting digit string `s`, return the number of distinct ways it can be decoded back into letters. Codes `"1"` through `"26"` are valid; nothing maps to `"0"`, and codes with a leading zero (like `"06"`) are invalid. If the string cannot be decoded at all, return `0`.

## Example 1

```
Input: s = "12"
Output: 2
```

`"12"` decodes as `"AB"` (1 | 2) or `"L"` (12).

## Example 2

```
Input: s = "226"
Output: 3
```

`"BZ"` (2 | 26), `"VF"` (22 | 6), `"BBF"` (2 | 2 | 6).

## Example 3

```
Input: s = "06"
Output: 0
```

`"06"` is not a valid code, and `"0"` alone maps to nothing.

## Constraints

- `1 <= len(s) <= 100`
- `s` contains only digits and may contain zeros

Watch the zeros: a `'0'` can only survive as the second digit of `"10"` or `"20"`.
