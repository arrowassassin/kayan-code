## Hint 1

"K closest" is "top k" with distance as the ranking key. Before reaching for any data structure, simplify the key itself: do you actually need the square root to decide which of two points is closer?

## Hint 2

Compare **squared** distances — `x² + y²` — since `sqrt` preserves order and integers avoid float issues. Now you want the k smallest keys out of n. If you keep a pool of k candidates while scanning, which element of the pool decides whether a new point gets in, and what heap orientation puts that element at the root?

## Hint 3

The pool's *worst* (largest-distance) member is the gatekeeper, so you need a **max-heap of size k** — in Python, a min-heap of `(-dist², x, y)`. Push until size k, then `heapreplace` whenever a point beats the root. O(n log k), O(k) space. Quickselect on squared distance gives average O(n) if the interviewer pushes.
