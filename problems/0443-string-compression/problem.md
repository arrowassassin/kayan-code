# String Compression

You are given a list of characters `chars`. Compress it **in place** using run-length encoding: each maximal run of a repeated character is replaced by the character followed by the run's length — except that runs of length 1 get no number at all.

Write the compressed form into the front of `chars` and return its length `k`. The judge will look at the first `k` entries of `chars` after your method returns; whatever sits beyond index `k-1` is ignored. Counts of 10 or more must be written as their individual digit characters (e.g. a run of 12 `'b'`s becomes `'b','1','2'`).

Use only **O(1) extra space** — building a separate string and copying it back is the thing this problem forbids.

## Example 1

```
Input: chars = ["a","a","b","b","c","c","c"]
Output: return 6, chars[:6] = ["a","2","b","2","c","3"]
```

## Example 2

```
Input: chars = ["a"]
Output: return 1, chars[:1] = ["a"]
```

A single character is not followed by a count.

## Example 3

```
Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: return 4, chars[:4] = ["a","b","1","2"]
```

The run of twelve `'b'`s compresses to `'b','1','2'`.

## Constraints

- `1 <= len(chars) <= 2000`
- `chars[i]` is a lowercase or uppercase English letter, a digit, or a simple symbol
- The compressed form is never longer than the original (guaranteed by the encoding rules)
