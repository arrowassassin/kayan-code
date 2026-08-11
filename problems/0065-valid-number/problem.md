# Valid Number

Decide whether a string `s` is a valid number. Return `True` or `False`.

A valid number is, in order:

1. optional leading and/or trailing **spaces** (the space character only — nothing else may surround the number, and no spaces may appear inside it);
2. an optional sign `+` or `-`;
3. a **decimal core**, which must contain at least one digit and takes one of these shapes:
   - digits (e.g. `7`, `0089`)
   - digits `.` (e.g. `3.`)
   - digits `.` digits (e.g. `12.5`)
   - `.` digits (e.g. `.9`)
4. an optional **exponent**: the letter `e` or `E`, an optional sign, then one or more digits.

Nothing else is allowed — no hex, no `inf`/`NaN`, no underscores, no second `.` or `e`. Leading zeros are fine (`0089`, `-090`). The whole string must be consumed: any leftover character makes it invalid.

## Example 1

```
Input: s = "-.9"
Output: true
```

Sign, then the `.digits` core.

## Example 2

```
Input: s = "4e+"
Output: false
```

The exponent has a sign but no digits.

## Example 3

```
Input: s = " 0.1 "
Output: true
```

Surrounding spaces are allowed; `0.1` is a valid decimal.

## Constraints

- `0 <= len(s) <= 300`
- `s` may contain letters, digits, `+`, `-`, `.`, and spaces
- An empty string, or a string of only spaces, is not a valid number
