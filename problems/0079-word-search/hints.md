## Hint 1

This is grid DFS — the Number of Islands walk — with one crucial difference: an island flood-fill marks cells visited *forever*, but here a cell blocked for one trace attempt may be needed by another. Start by writing the plain DFS: from every cell, try to match the word one character deeper per step.

## Hint 2

`dfs(r, c, k)` asks: can `word[k:]` be traced starting at `(r, c)`? Fail fast if the cell doesn't match `word[k]`; succeed if it matches and `k` is the last index. Otherwise mark `(r, c)` as in-use and try the four neighbors with `k + 1`. The question is what "mark" must mean here.

## Hint 3

Mark by overwriting `board[r][c]` with a sentinel like `'#'` (no letter equals it, so revisits fail the character test automatically) — and **restore the original character before returning**, on the failure path *and* on the success path. That restore is the backtracking: without it, cells consumed by a failed attempt stay poisoned and a later valid trace through them is wrongly rejected. No separate visited set needed.
