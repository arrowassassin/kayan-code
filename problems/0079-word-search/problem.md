# Word Search

You are given a rectangular grid `board` of single characters and a string `word`. Decide whether `word` can be traced in the grid by starting at any cell and repeatedly stepping to a **horizontally or vertically adjacent** cell, reading one character per cell.

A cell may be used **at most once** within a single trace. Return `True` if some trace spells `word`, otherwise `False`.

## Example 1

```
Input: board = [["A","B","C","E"],
                ["S","F","C","S"],
                ["A","D","E","E"]],
       word = "ABCCED"
Output: true
```

Start at the top-left `A`, move right to `B`, `C`, down to the second `C`, down to `E`, left to `D`.

## Example 2

```
Input: board = [["A","B","C","E"],
                ["S","F","C","S"],
                ["A","D","E","E"]],
       word = "ABCB"
Output: false
```

The only `B` adjacent to the second `C`'s neighborhood is the one already used — cells cannot be revisited.

## Constraints

- `1 <= rows, cols <= 6`
- `1 <= len(word) <= 12`
- `board` and `word` consist of uppercase and lowercase English letters only

Matching is case-sensitive. The same cell may appear in *different* trace attempts — the no-revisit rule applies only within one trace.
