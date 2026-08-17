# Generate Parentheses

Given an integer `n`, return **all** distinct strings made of exactly `n` opening and `n` closing parentheses that are **well-formed** — every prefix of the string has at least as many `(` as `)`, and the whole string is balanced.

Return the strings in **any order**.

## Example 1

```
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```

## Example 2

```
Input: n = 1
Output: ["()"]
```

## Constraints

- `1 <= n <= 8`

The number of well-formed strings grows like the Catalan numbers (n = 8 gives 1,430), which is why `n` is capped so low.
