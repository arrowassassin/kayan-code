# Most Common Word

You are given a paragraph of text and a list of banned words. Return the most frequent word in the paragraph that is **not** banned. The answer is guaranteed to exist and to be unique.

Rules of the road:

- Comparison is case-insensitive; return the answer in **lowercase**.
- Words are separated by spaces and/or punctuation (`! ? ' , ; .`). Punctuation glued onto a word (`"ball,"`) is not part of the word.
- The banned list is given in lowercase, and banned words are counted as if they don't exist — they can never be the answer no matter how often they appear.

## Example 1

```
Input: paragraph = "Bob hit a ball, the hit BALL flew far after it was hit.", banned = ["hit"]
Output: "ball"
```

`"hit"` appears three times but is banned; `"ball"` appears twice (`"ball,"` and `"BALL"` both count as `ball`).

## Example 2

```
Input: paragraph = "a.", banned = []
Output: "a"
```

## Constraints

- `1 <= len(paragraph) <= 1000`
- `paragraph` consists of English letters, spaces, and the punctuation characters `! ? ' , ; .`
- `0 <= len(banned) <= 100`, each banned word is 1–10 lowercase letters
- At least one non-banned word exists in the paragraph, and the most frequent one is unique
