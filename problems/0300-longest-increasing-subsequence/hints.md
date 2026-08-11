## Hint 1

Brute force enumerates all 2^n subsequences — hopeless. Instead, anchor the problem: for each index `i`, ask "what is the longest strictly increasing subsequence that **ends exactly at** `nums[i]`?" Anchoring at the last element makes subproblems combinable.

## Hint 2

If the best subsequence ending at `i` has length `L`, its second-to-last element is some `j < i` with `nums[j] < nums[i]` — and the prefix ending at `j` must itself be optimal. So `dp[i] = 1 + max(dp[j] for j < i with nums[j] < nums[i])`, default 1. That's O(n^2); the answer is `max(dp)`.

## Hint 3

For O(n log n): keep `tails`, where `tails[k]` is the *smallest possible tail* of any increasing subsequence of length `k+1`. This list stays sorted, so each new number either extends it (append) or improves one entry — found by binary search (`bisect_left` for strict increase). The final length of `tails` is the answer.
