# Text Justification

Given a list of `words` and a line width `maxWidth`, typeset the words into fully justified lines and return the lines as a list of strings. Every returned line must be exactly `maxWidth` characters long.

Packing rule (greedy): put as many words on each line as fit, given that words on a line are separated by at least one space.

Spacing rules:

- **Full lines** (every line except the last, when it holds 2+ words): distribute the leftover spaces as evenly as possible between the words. When the spaces don't divide evenly, the **leftmost gaps get the extra space** — gap sizes never differ by more than one, decreasing left to right.
- **Single-word lines**: the word, then spaces to fill the width.
- **The last line**: left-justified — words separated by exactly one space, then spaces to fill the width.

## Example 1

```
Input: words = ["This","is","an","example","of","text","justification."], maxWidth = 16
Output:
[
  "This    is    an",
  "example  of text",
  "justification.  "
]
```

## Example 2

```
Input: words = ["What","must","be","acknowledgment","shall","be"], maxWidth = 16
Output:
[
  "What   must   be",
  "acknowledgment  ",
  "shall be        "
]
```

`"acknowledgment"` sits alone on a full line, so it is left-justified like a single-word line; `"shall be"` is the last line.

## Constraints

- `1 <= len(words) <= 300`
- `1 <= len(words[i]) <= 20`
- `1 <= maxWidth <= 100`
- `len(words[i]) <= maxWidth` for every word
- Words consist of visible ASCII characters (no spaces inside a word)
