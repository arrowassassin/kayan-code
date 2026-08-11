## Hint 1

Try the standard sliding window directly on "exactly k distinct" and watch it fail: when the window holds exactly k distinct values, you know neither whether to grow (might stay at k) nor to shrink (might drop to k-1). The property isn't monotone in window length — that's the wall this problem is built around.

## Hint 2

"**At most** k distinct" *is* monotone, and you already know how to window it (Fruit Into Baskets is the k=2 case). Bonus: an at-most window can *count* subarrays — when the window `[left, right]` is valid, every subarray ending at `right` and starting at `left` or later is also valid. How many is that per step?

## Hint 3

`at_most(k)` = sum over `right` of `right - left + 1`, with the usual shrink-while-more-than-k-distinct loop. Then use inclusion–exclusion on the answer itself: subarrays with exactly k distinct = `at_most(k) - at_most(k-1)`. Two passes of code you already have from the warmup.
