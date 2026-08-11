# Compare Version Numbers

You are given two version strings, `version1` and `version2`, each made of numeric chunks joined by dots (e.g. `"1.01.3"`). Compare them chunk by chunk, left to right:

- Each chunk is compared as an **integer**, so leading zeros are irrelevant: `"01"` and `"001"` both mean `1`.
- If one version runs out of chunks, its missing chunks count as `0`: `"1.0"` and `"1.0.0.0"` are equal.

Return `-1` if `version1 < version2`, `1` if `version1 > version2`, and `0` if they are equal.

## Example 1

```
Input: version1 = "1.01", version2 = "1.001"
Output: 0
```

`01` and `001` are both the integer 1.

## Example 2

```
Input: version1 = "1.0", version2 = "1.0.0"
Output: 0
```

The missing third chunk of `version1` counts as 0.

## Example 3

```
Input: version1 = "0.1", version2 = "1.1"
Output: -1
```

The first chunks already decide: `0 < 1`.

## Constraints

- `1 <= len(version1), len(version2) <= 500`
- Both strings contain only digits and dots; they never start or end with a dot, and never have two dots in a row
- Every chunk fits in a 32-bit signed integer (but chunks may carry many leading zeros)
