## Hint 1

Trying every way to peel words off the front is correct but explodes: on `"aaaa...b"` with dictionary `["a","aa","aaa",...]` the same suffixes get re-explored exponentially often. How many *distinct* suffixes (or prefixes) of `s` are there, really?

## Hint 2

Whether the rest of the string can be broken depends only on **where you are**, not on which words got you there. So define `dp[i]` = "the prefix `s[:i]` can be segmented" — a single boolean per position, `n+1` states total.

## Hint 3

`dp[0] = True` (empty prefix). `dp[i]` is true if some `j < i` has `dp[j]` true and `s[j:i]` in the dictionary — i.e. a breakable prefix plus one final dictionary word. Put the words in a set for O(1) lookup, and only scan `j` back as far as the longest word's length. Answer: `dp[n]`.
