# Word Break

Given a string `s` and a list of dictionary words `wordDict`, decide whether `s` can be split into a sequence of one or more dictionary words with nothing left over.

Each dictionary word may be reused any number of times. Return `True` or `False`.

## Example 1

```
Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
```

`"leetcode" = "leet" + "code"`.

## Example 2

```
Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
```

`"apple" + "pen" + "apple"` — reuse is allowed.

## Example 3

```
Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false
```

Every split strands at least one letter (`"catsand" + "og"`, `"cats" + "andog"`, ...).

## Constraints

- `1 <= len(s) <= 300`
- `1 <= len(wordDict) <= 1000`
- `1 <= len(wordDict[i]) <= 20`
- `s` and all dictionary words consist of lowercase English letters
- All dictionary words are distinct
