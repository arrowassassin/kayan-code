# Reorder Data in Log Files

Each entry in `logs` is a space-separated line: an **identifier** (the first token, made of letters and digits) followed by the log's content. Content comes in two flavors:

- **letter-logs** — every content token consists of lowercase letters;
- **digit-logs** — every content token consists of digits.

Rearrange the logs so that:

1. All letter-logs come before all digit-logs.
2. Letter-logs are ordered lexicographically by their **content** (identifier excluded); if two letter-logs have identical content, order them lexicographically by identifier.
3. Digit-logs keep their **original relative order**.

Return the reordered list.

## Example 1

```
Input: logs = ["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
Output: ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]
```

`"art can" < "art zero" < "own kit dig"`; the two digit-logs stay in input order.

## Example 2

```
Input: logs = ["j mo","5 m w"]
Output: ["5 m w","j mo"]
```

Careful: `"j mo"` has letter content, `"5 m w"` — identifier `5`, content `m w` — is a **letter-log** too, and `"m w" < "mo"` lexicographically (space sorts before `o`).

## Constraints

- `1 <= len(logs) <= 100`
- `3 <= len(logs[i]) <= 100`
- Every log has an identifier and at least one content token
- Content tokens are all-letters or all-digits (never mixed within one log)

The identifier may contain digits even for a letter-log — only the content decides the flavor.
