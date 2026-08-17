# Combination Sum

You are given a list `candidates` of **distinct** positive integers and a positive integer `target`. Return every **unique combination** of candidates whose values sum to exactly `target`. The same candidate may be used **any number of times** within a combination.

Two combinations are the same if they use the same multiset of values — `[2,2,3]` and `[3,2,2]` count as one combination, and only one of them may appear in your answer. Combinations may be returned in **any order**.

## Example 1

```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
```

`2 + 2 + 3 = 7` (2 is reused) and `7 = 7`. No other multiset of these candidates reaches 7.

## Example 2

```
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
```

## Example 3

```
Input: candidates = [2], target = 1
Output: []
```

## Constraints

- `1 <= len(candidates) <= 30`
- `2 <= candidates[i] <= 40` — all values distinct
- `1 <= target <= 40`

Since every candidate is at least 2, any valid combination has at most 20 elements — the test data guarantees fewer than 150 combinations per case.
