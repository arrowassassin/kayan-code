## Hint 1

Comparing all subsequences of one string against the other is doubly exponential. When a problem involves *two* sequences, the standard move is a state with one index into each: think about the pair of prefixes `text1[:i]`, `text2[:j]`.

## Hint 2

Look at the *last* characters of the two prefixes. If they are equal, they can safely end the common subsequence — take them and shrink both prefixes. If they differ, at least one of them is useless: the answer drops one character from `text1` or from `text2`, whichever is better.

## Hint 3

`dp[i][j]` = LCS length of `text1[:i]` and `text2[:j]`. Match: `dp[i][j] = dp[i-1][j-1] + 1`; mismatch: `max(dp[i-1][j], dp[i][j-1])`; row/column 0 are all 0. Fill row by row — and notice each row only reads the previous one, so two rows (or one, with care) of length `n+1` suffice.
