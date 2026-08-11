# Count Vowel Substrings of a String

A substring is a contiguous, non-empty slice of a string. Call a substring a **vowel substring** if two things hold at once:

1. every character in it is a vowel (`a`, `e`, `i`, `o`, `u`), and
2. all five vowels each appear at least once inside it.

Given a lowercase string `word`, return the number of vowel substrings it contains. Two substrings taken from different positions count separately even if their text is identical.

## Example 1

```
Input: word = "aeiouu"
Output: 2
```

The qualifying substrings are `"aeiou"` (indices 0–4) and `"aeiouu"` (indices 0–5). Shorter slices are missing at least one vowel.

## Example 2

```
Input: word = "cuaieuouac"
Output: 7
```

Every qualifying substring lives strictly between the two `c`s; seven different slices of that vowel block contain all five vowels.

## Example 3

```
Input: word = "duckgoose"
Output: 0
```

No substring avoids consonants while containing all five vowels.

## Constraints

- `1 <= len(word) <= 100`
- `word` consists of lowercase English letters only

A single consonant anywhere inside a slice disqualifies it; repeated vowels are fine as long as all five distinct vowels show up.
