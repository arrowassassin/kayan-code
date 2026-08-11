## Hint 1

Unsorted input, but the answer is defined by *values*, not positions — so nothing stops you from sorting first. Once sorted, "find two values with a given sum" is a problem you have already solved (Two Sum II).

## Hint 2

Fix the smallest element of the triplet with an outer loop over index `i`. The remaining task is exactly Two Sum II on the suffix `nums[i+1:]` with target `-nums[i]` — a converging two-pointer scan, no hash map.

## Hint 3

Deduplication comes from the sort, not from a set: skip `i` when `nums[i] == nums[i-1]`, and after recording a match, advance `lo` past every copy of `nums[lo]` before continuing. Also, once `nums[i] > 0` you can stop the outer loop entirely — three positives can't sum to zero.
