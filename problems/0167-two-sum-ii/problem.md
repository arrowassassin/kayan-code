# Two Sum II — Input Array Is Sorted

You are given an array `numbers` sorted in **non-decreasing** order and an integer `target`. Exactly one pair of elements `numbers[i]` and `numbers[j]` (with `i < j`) adds up to `target` — find it.

Return the two positions as **1-indexed** values `[i+1, j+1]`, smaller index first.

Your solution must use **O(1) extra space** — the hash-map trick from classic Two Sum is off the table.

## Example 1

```
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
```

`numbers[0] + numbers[1] = 2 + 7 = 9`, so the 1-indexed answer is `[1,2]`.

## Example 2

```
Input: numbers = [-1,0,2,5], target = 4
Output: [1,4]
```

`-1 + 5 = 4` at 1-indexed positions 1 and 4.

## Example 3

```
Input: numbers = [1,1], target = 2
Output: [1,2]
```

## Constraints

- `2 <= len(numbers) <= 10^5`
- `-10^4 <= numbers[i] <= 10^4`
- `numbers` is sorted in non-decreasing order (duplicates allowed)
- `-2 * 10^4 <= target <= 2 * 10^4`
- Exactly one valid pair exists; an element may not be used twice
