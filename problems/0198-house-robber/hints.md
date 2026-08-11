## Hint 1

Greedy fails: "rob every other house" gives 3 on `[2,1,1,2]` but the answer is 4, and "grab the richest house first" also breaks. When each choice constrains the next one, define the best answer for every *prefix* of the street instead of deciding houses in isolation.

## Hint 2

Stand at house `i` and say the choice out loud: either you **rob it** (then house `i-1` must be skipped, so you add `nums[i]` to the best answer for the first `i-1` houses... minus one more) or you **skip it** (the best answer for the first `i-1` houses carries over). That sentence *is* the recurrence.

## Hint 3

Let `dp[i]` = max cash from the first `i` houses. Then `dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])` with `dp[0] = dp[1] = ...` base cases you can read off directly. Only the last two values are ever consulted, so two rolling variables suffice — O(n) time, O(1) space.
