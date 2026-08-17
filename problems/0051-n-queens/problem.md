# N-Queens

Place `n` chess queens on an `n × n` board so that no two queens attack each other — no two share a row, a column, or a diagonal. Return **all** distinct solutions, in **any order**.

Each solution is the board drawn as a list of `n` strings of length `n`, where `'Q'` marks a queen and `'.'` an empty square.

## Example 1

```
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],
         ["..Q.","Q...","...Q",".Q.."]]
```

The two 4×4 solutions are mirror images of each other.

## Example 2

```
Input: n = 1
Output: [["Q"]]
```

## Constraints

- `1 <= n <= 9`

`n = 2` and `n = 3` have no solutions — return an empty list. The solution count grows explosively (n = 9 has 352), hence the small cap.
