## Hint 1

Don't search the piles — search the *answer*. The unknown is a single integer `k`, and for any candidate `k` you can cheaply check whether it's fast enough. What are the smallest and largest speeds worth considering?

## Hint 2

The feasibility check is monotonic: if speed `k` finishes within `h` hours, then every speed above `k` does too, and if `k` fails, everything below it fails. That splits the range `1..max(piles)` into a "too slow" prefix and a "works" suffix — exactly the shape binary search needs.

## Hint 3

Write `hours_at(k) = sum(ceil(p / k) for p in piles)` — an O(n) predicate. Binary search the smallest `k` in `[1, max(piles)]` with `hours_at(k) <= h`: when the check passes, keep `mid` in range (`hi = mid`); when it fails, discard it (`lo = mid + 1`); stop when `lo == hi`. Use `(p + k - 1) // k` for the ceiling division.
