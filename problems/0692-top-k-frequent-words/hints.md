## Hint 1

Structurally this is Top K Frequent Elements again — count with a hash map, then rank. What changed is the *ranking rule*: two criteria instead of one, pulling in opposite directions (bigger frequency is better, but smaller word is better).

## Hint 2

Python compares tuples field by field. If you can build a single key per word such that "better" always means "smaller key", then any smallest-k machinery — a sort, or `heapq.nsmallest` — produces the required order directly. How do you flip "bigger frequency is better" into "smaller is better"? Frequencies are numbers; words are not.

## Hint 3

Use the key `(-count, word)`: negating the count makes higher frequency sort first, and the word itself breaks ties alphabetically. Then either sort the distinct words by that key and slice `k` (O(d log d)), or feed it to `heapq.nsmallest(k, ...)` for O(d log k). Note you can negate a number but not a string — that's why the trick is to negate the count rather than reverse the word.
