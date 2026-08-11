## Hint 1

Sorting the whole array answers a much bigger question than the one asked — you only need one rank. What structures let you track "the k biggest so far" without ordering everything?

## Hint 2

Keep a container of exactly `k` candidates while scanning. When a new number arrives, you only care whether it beats the *weakest* of the current candidates — so you need cheap access to the minimum of the kept set. That is precisely what a **min-heap** of size `k` gives you: its root is the k-th largest seen so far.

## Hint 3

Scan once: push each value, and whenever the heap exceeds size `k`, pop the root — O(n log k). Alternatively, partition the array quicksort-style around a random pivot and recurse **only into the side containing the target index** (quickselect): O(n) average. Know both, and know which one degrades on adversarial input.
