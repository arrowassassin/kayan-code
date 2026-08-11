## Hint 1

This is House Robber with the street stretched: each "house" is a job, and "adjacent" means "overlapping in time". In House Robber, robbing house `i` sent you back to `i-2`; here, taking a job sends you back to... which job? Sorting by something should make that question answerable.

## Hint 2

Sort jobs by **end time** and define `dp[k]` = best profit using only the first `k` jobs. Job `k` is either skipped (`dp[k-1]`) or taken — and if taken, everything else must end **at or before** its start time. Because the jobs are sorted by end, "the best set ending by time `t`" is a prefix answer you have already computed.

## Hint 3

Binary search makes "latest job ending <= my start" an O(log n) lookup: keep parallel arrays `ends` (increasing) and `best` (increasing), and for each job in end-time order do `i = bisect_right(ends, start) - 1`, `take = best[i] + profit`. Append `(end, take)` only when `take` beats the current maximum, so both arrays stay sorted. O(n log n) total — the O(n^2) "scan backward for a compatible job" version times out at n = 5 * 10^4.
