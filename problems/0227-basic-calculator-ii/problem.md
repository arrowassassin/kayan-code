# Basic Calculator II

Evaluate an arithmetic expression given as a string `s` and return its value as an integer.

The expression contains non-negative integers and the four operators `+`, `-`, `*`, `/`, possibly with spaces sprinkled anywhere between tokens. Usual precedence applies: `*` and `/` bind tighter than `+` and `-`, and operators of equal precedence evaluate left to right. There are **no** parentheses and no unary operators.

Division is **integer division that truncates toward zero** — so an intermediate result of `-3 / 2` gives `-1`, not `-2`. Numbers in `s` are all non-negative; negatives only arise as intermediate values (e.g. after a subtraction).

You may not use `eval` or any expression-evaluation library.

## Example 1

```
Input: s = "3+2*2"
Output: 7
```

Multiplication first: `3 + 4`.

## Example 2

```
Input: s = " 3+5 / 2 "
Output: 5
```

`5 / 2` truncates to `2`.

## Example 3

```
Input: s = "1-3*2"
Output: -5
```

## Constraints

- `1 <= len(s) <= 3 * 10^5`
- `s` consists of digits, `+`, `-`, `*`, `/` and spaces
- All numbers in `s` fit in a 32-bit signed integer, and so do all intermediate results
- `s` is a valid expression; division by zero never occurs
