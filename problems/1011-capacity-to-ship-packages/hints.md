## Hint 1

This is Koko Eating Bananas in a shipping costume: the unknown is one number (the capacity), and for any candidate capacity you can quickly test whether the schedule fits in `days`. What range of capacities could possibly be the answer?

## Hint 2

If capacity `c` gets everything shipped in time, then `c + 1` certainly does too — the feasibility of the answer space is monotonic, so binary search the capacity between `max(weights)` (anything smaller can't carry the heaviest package) and `sum(weights)` (ships it all in one day).

## Hint 3

The check itself is a greedy one-pass simulation: walk the belt in order, adding weights to the current day; when the next package would overflow the candidate capacity, start a new day. Count days and compare to `days`. Greedy is safe here because packages are contiguous — postponing a package never helps. Bisect for the smallest capacity whose day count fits.
