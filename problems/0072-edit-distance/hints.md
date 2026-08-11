## Hint 1

Don't think about *sequences* of edits — think about what the edits do to the **ends** of the strings. Compare the last character of `word1` with the last character of `word2`: either they already agree, or exactly one operation must deal with the mismatch.

## Hint 2

Define `dp[i][j]` = minimum edits turning `word1[:i]` into `word2[:j]`. If the last characters match, no operation is needed there: `dp[i][j] = dp[i-1][j-1]`. If they differ, one operation fixes the boundary in one of three ways — replace (both prefixes shrink), delete from `word1` (only `i` shrinks), insert into `word1` (only `j` shrinks) — take `1 + min` of the three.

## Hint 3

Base cases are the empty-string borders: `dp[i][0] = i` (delete everything), `dp[0][j] = j` (insert everything). Fill the table row by row; each row reads only the previous row plus its own left neighbor, so two rolling rows give O(min(m,n)) space. Answer: `dp[m][n]`.
