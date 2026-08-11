# Valid Palindrome II

Given a string `s`, decide whether it can be turned into a palindrome by deleting **at most one** character. Deleting zero characters is allowed — a string that is already a palindrome qualifies.

Return `True` or `False`.

## Example 1

```
Input: s = "aba"
Output: True
```

Already a palindrome; no deletion needed.

## Example 2

```
Input: s = "abca"
Output: True
```

Delete the `c` (or the `b`... only the `c` works — check!) to get `"aba"`.

## Example 3

```
Input: s = "abc"
Output: False
```

No single deletion produces a palindrome.

## Constraints

- `1 <= len(s) <= 10^5`
- `s` consists of lowercase English letters only
