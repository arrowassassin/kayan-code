# Valid Palindrome

Given a string `s`, decide whether it reads the same forwards and backwards **after** you (a) drop every character that is not a letter or digit and (b) ignore letter case.

Return `True` if the cleaned-up string is a palindrome, `False` otherwise. A string that becomes empty after cleaning counts as a palindrome.

## Example 1

```
Input: s = "A man, a plan, a canal: Panama"
Output: true
```

Keeping only alphanumerics and lowercasing gives `"amanaplanacanalpanama"`, which is a palindrome.

## Example 2

```
Input: s = "race a car"
Output: false
```

`"raceacar"` is not a palindrome.

## Example 3

```
Input: s = ".,"
Output: true
```

Nothing survives the cleaning, and the empty string is a palindrome.

## Constraints

- `0 <= len(s) <= 2 * 10^5`
- `s` consists of printable ASCII characters (letters, digits, punctuation, spaces)

Digits count as characters to compare: `"0P"` is **not** a palindrome, while `"12321"` is.
