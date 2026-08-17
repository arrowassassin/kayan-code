# Implement Trie (Prefix Tree)

A **trie** (prefix tree) stores a set of strings so that lookups by whole word *or by prefix* are fast. Implement the class `Trie`:

- `Trie()` — create an empty trie.
- `insert(word)` — add `word` to the trie.
- `search(word) -> bool` — return `True` iff `word` was previously inserted as a **complete word**.
- `startsWith(prefix) -> bool` — return `True` iff at least one previously inserted word has `prefix` as a prefix. (Every word is a prefix of itself.)

Inserting the same word more than once has no additional effect.

## Example

```
Trie trie = Trie()
trie.insert("apple")
trie.search("apple")      # returns True
trie.search("app")        # returns False  ("app" was never inserted as a word)
trie.startsWith("app")    # returns True   ("apple" starts with "app")
trie.insert("app")
trie.search("app")        # returns True
```

## Constraints

- `1 <= len(word), len(prefix) <= 2000`
- All strings consist of lowercase English letters `a`–`z`
- Up to `3 * 10^4` calls in total to `insert`, `search`, and `startsWith`
- The sum of all argument lengths does not exceed `5 * 10^5`
