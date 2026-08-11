## Hint 1

"Shortest contiguous subarray meeting a threshold" over **positive** numbers — positivity is the loud hint. What does adding an element always do to the window sum? What does removing one always do? That pair of guarantees enables a two-pointer window.

## Hint 2

Because every element is positive, the window sum is strictly monotone: growing the window always increases it, shrinking always decreases it. So once the window's sum reaches `target`, extending it further can never produce a *shorter* valid answer — shrink instead.

## Hint 3

Expand `right`, adding to a running sum. While the sum is `>= target`, record the current length as a candidate, subtract `nums[left]`, and advance `left`. Return 0 if no window ever qualified. (Also worth knowing: prefix sums + binary search give an O(n log n) alternative — and if negatives were allowed, the window would be invalid and prefix-based methods would be the *only* option.)
