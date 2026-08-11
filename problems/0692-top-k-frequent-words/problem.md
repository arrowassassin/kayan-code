# Top K Frequent Words

Given a list of lowercase strings `words` and an integer `k`, return the `k` words that appear most often — but unlike the integer version, the output order is **fully specified**:

- more frequent words come first;
- among words with equal frequency, the **alphabetically smaller** word comes first.

## Example 1

```
Input: words = ["the","sky","is","blue","the","sky","the"], k = 2
Output: ["the","sky"]
```

`"the"` appears 3 times, `"sky"` twice.

## Example 2

```
Input: words = ["apple","pear","apple","pear","fig"], k = 2
Output: ["apple","pear"]
```

`"apple"` and `"pear"` are tied at 2 occurrences; `"apple"` wins the tie alphabetically.

## Constraints

- `1 <= len(words) <= 5 * 10^4`
- `1 <= len(words[i]) <= 10` — lowercase English letters only
- `1 <= k <=` number of distinct words
