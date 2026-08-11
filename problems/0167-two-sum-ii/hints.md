## Hint 1

The array is sorted and the classic hash-map answer is banned by the O(1)-space requirement. What does sortedness let you *predict* about where a bigger or smaller sum lives?

## Hint 2

Place one pointer at each end. Their sum is either correct, too small, or too big — and in each of the wrong cases, exactly one pointer has no future: if the sum is too small, the left value paired with the *largest* remaining value still fell short, so the left value can never be part of the answer.

## Hint 3

Loop while `lo < hi`: on `sum < target` advance `lo`, on `sum > target` retreat `hi`, on equality return `[lo + 1, hi + 1]` (1-indexed!). Each step permanently discards one element, so the scan is a single O(n) pass.
