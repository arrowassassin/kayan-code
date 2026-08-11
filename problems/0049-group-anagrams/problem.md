# Group Anagrams

Two strings are anagrams if one can be rearranged into the other — same letters, same multiplicities, different order allowed. Given a list of strings `strs`, bundle the anagrams together: return a list of groups, where each group contains every string from the input that is an anagram of the others in that group.

Groups may be returned in any order, and the strings within a group may be in any order. Every input string (including duplicates) must appear in exactly one group.

## Example 1

```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["eat","tea","ate"],["tan","nat"],["bat"]]
```

## Example 2

```
Input: strs = [""]
Output: [[""]]
```

The empty string forms its own (single-member) group.

## Constraints

- `1 <= len(strs) <= 10^4`
- `0 <= len(strs[i]) <= 100`
- `strs[i]` consists of lowercase English letters only
- Duplicate strings may occur, and each occurrence must be placed in the group
