## Hint 1

Simulating every path move-by-move blows up — path counts grow combinatorially. Instead ask a local question: how can the robot possibly *arrive* at a given cell?

## Hint 2

Only two ways in: from the cell above, or from the cell to the left. Every path to those two cells extends uniquely into this one, and no path is counted twice — so `paths(r, c) = paths(r-1, c) + paths(r, c-1)`, with one path to every cell in the first row and first column.

## Hint 3

Fill the grid row by row; each row only reads itself and the previous row, so a single 1-D array of length `n` suffices: `row[j] += row[j-1]`. Bonus: every path is a shuffle of `m-1` downs among `m+n-2` total moves — the closed form `C(m+n-2, m-1)` — but derive the DP first; it's what generalizes.
