## Hint 1

Greedy (always take the largest coin that fits) is wrong — `coins = [1,3,4]`, `amount = 6` gives `4+1+1` instead of `3+3`. When greedy fails on a "fewest steps to reach a target" question, ask: what is the fewest number of coins for every *smaller* amount?

## Hint 2

Whatever the optimal combination for `amount` is, it has a *last* coin `c`. Remove it and what remains must be an optimal combination for `amount - c` — otherwise you could improve the whole. So: `fewest(a) = 1 + min over coins c of fewest(a - c)`.

## Hint 3

Fill `dp[0..amount]` left to right with `dp[0] = 0` and `dp[a] = min(dp[a - c] + 1 for every coin c <= a)`. Use a sentinel like `amount + 1` for "unreachable"; if it survives at `dp[amount]`, return `-1`. O(amount × len(coins)) time.
