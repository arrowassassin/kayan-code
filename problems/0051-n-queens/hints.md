## Hint 1

Don't search over all n² squares. Every valid solution has exactly one queen **per row** — so a solution is just a choice of one column for each row, and you can build it row by row, top to bottom. What does that reduce the search space to?

## Hint 2

When you're placing the queen for row `r`, earlier rows are fixed. Column clashes are easy to check with a set of used columns. For diagonals, find a single number that is constant along a "\" diagonal, and another constant along a "/" diagonal — look at what happens to `r - c` and `r + c` as you step diagonally.

## Hint 3

Keep three sets: `cols`, `diag` (keys `r - c`), `anti` (keys `r + c`). For each candidate column in row `r`: if all three keys are free — add them and the column choice, recurse to row `r + 1`, then remove all three and pop the choice (the unchoose step must undo *everything* the choose step did). When `r == n`, convert the list of chosen columns into the string board. Rows can never clash by construction.
