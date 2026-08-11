# Edit Distance

Given two strings `word1` and `word2`, return the minimum number of single-character operations needed to transform `word1` into `word2`.

Three operations are allowed, each costing 1:

- **Insert** a character anywhere
- **Delete** any character
- **Replace** any character with another

## Example 1

```
Input: word1 = "horse", word2 = "ros"
Output: 3
```

`horse -> rorse` (replace `h` with `r`), `rorse -> rose` (delete `r`), `rose -> ros` (delete `e`).

## Example 2

```
Input: word1 = "intention", word2 = "execution"
Output: 5
```

## Constraints

- `0 <= len(word1), len(word2) <= 500`
- Both strings consist of lowercase English letters only

Either string may be empty: transforming from or to `""` costs one operation per character of the other string.
