## Hint 1

Rephrase before solving: two groups with equal sums exist iff some subset sums to exactly `total / 2` (the rest automatically forms the other group). And if `total` is odd, you can answer immediately.

## Hint 2

"Does any subset hit a target sum?" is 0/1 knapsack. Process numbers one at a time and track the set of sums that are *achievable so far* — each new number either joins the subset (shifting an achievable sum up by its value) or doesn't.

## Hint 3

Boolean table `dp[s]` = "sum `s` achievable", `dp[0] = True`. For each number `x`, update `s` from `target` **down** to `x`: `dp[s] |= dp[s - x]`. The downward sweep is what stops one number from being used twice. Return `dp[target]` — and feel free to early-exit the moment it flips.
