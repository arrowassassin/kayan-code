# Reverse Words in a String

You are given a string `s` containing words separated by spaces. Reverse the **order of the words** (not the letters inside them) and return the result as a single string in which:

- words appear in reverse order, separated by exactly **one** space,
- there are no leading or trailing spaces.

The input is messy: `s` may begin or end with spaces, and words may be separated by runs of several spaces. A *word* is any maximal run of non-space characters.

## Example 1

```
Input: s = "the sky is blue"
Output: "blue is sky the"
```

## Example 2

```
Input: s = "  hello world  "
Output: "world hello"
```

Leading and trailing spaces disappear.

## Example 3

```
Input: s = "a good   example"
Output: "example good a"
```

The triple space collapses to a single one.

## Constraints

- `1 <= len(s) <= 10^4`
- `s` consists of printable ASCII characters and spaces (`' '` only — no tabs or newlines)
- `s` contains at least one word

Words may contain digits and punctuation — anything that isn't a space belongs to the word.
