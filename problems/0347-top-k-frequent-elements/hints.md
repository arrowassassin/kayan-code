## Hint 1

Two separate jobs are hiding in this problem: first *measure* something (how often each value appears), then *rank* by that measurement. Solve the measuring step with a hash map before worrying about the ranking step.

## Hint 2

Once you hold `{value: count}` pairs, this is exactly Kth Largest in disguise — pick the k pairs with the biggest counts. A heap bounded at size `k` over the counts gives O(n log k). But look at what you're ranking: counts are integers between 1 and `len(nums)`. A *bounded* key range should make you think of something faster than comparisons.

## Hint 3

Bucket sort on frequency: make `len(nums)+1` buckets, drop each value into `buckets[count]`, then walk the buckets from the highest frequency down, collecting values until you have `k`. Every step is a linear scan — O(n) total, no heap, no sort.
