# Word Ladder

You are given two words `beginWord` and `endWord` of the same length, plus a dictionary `wordList`. A **transformation sequence** is a chain of words starting at `beginWord` where:

- each word differs from the previous one in **exactly one letter**, and
- every word after `beginWord` (including `endWord`) appears in `wordList`.

Return the **length of the shortest** transformation sequence from `beginWord` to `endWord`, counted in words (so the chain `hit -> hot -> dot -> dog -> cog` has length 5). If no chain exists, return `0`.

`beginWord` itself does not need to be in `wordList`.

## Example 1

```
Input: beginWord = "hit", endWord = "cog",
       wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
```

One shortest chain: `hit -> hot -> dot -> dog -> cog`.

## Example 2

```
Input: beginWord = "hit", endWord = "cog",
       wordList = ["hot","dot","dog","lot","log"]
Output: 0
```

`cog` is not in the dictionary, so no valid chain can end there.

## Constraints

- `1 <= len(beginWord) <= 10`
- All words have the same length as `beginWord` and consist of lowercase English letters
- `1 <= len(wordList) <= 5000`, all entries distinct
- `beginWord != endWord`
