# Decode String

A string has been compressed with the rule `k[chunk]`, meaning "`chunk`, repeated `k` times". The rule may nest: the chunk inside the brackets can itself contain further `k[...]` blocks, as well as ordinary letters.

Given a valid encoded string `s`, return the decoded string.

Guarantees: `s` is always well-formed (brackets balance, every `[` is immediately preceded by a positive integer), digits appear **only** as repeat counts, and counts may have several digits (e.g. `12[ab]`).

## Example 1

```
Input: s = "3[a]2[bc]"
Output: "aaabcbc"
```

## Example 2

```
Input: s = "3[a2[c]]"
Output: "accaccacc"
```

The inner block expands first: `a2[c]` → `acc`, then repeat three times.

## Example 3

```
Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
```

Plain letters outside any brackets pass through unchanged.

## Constraints

- `1 <= len(s) <= 100`
- `s` consists of lowercase English letters, digits, and square brackets `[]`
- All repeat counts are integers in `[1, 300]`
- The decoded output is guaranteed to have at most `2 * 10^5` characters
