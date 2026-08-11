# K Closest Points to Origin

You are given a list of `points` on the plane, where `points[i] = [x, y]`, and an integer `k`. Return the `k` points nearest to the origin `(0, 0)` measured by Euclidean distance.

The answer may be returned **in any order**. The test data guarantees the answer is unique: no point outside the answer is at the same distance as a point inside it.

## Example 1

```
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
```

`[-2,2]` is at distance √8 ≈ 2.83; `[1,3]` is at √10 ≈ 3.16.

## Example 2

```
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
```

Distances squared are 18, 26 and 20 — the two smallest are `[3,3]` and `[-2,4]`. `[[-2,4],[3,3]]` is also accepted.

## Constraints

- `1 <= k <= len(points) <= 10^5`
- `-10^4 <= x, y <= 10^4`
- The set of k closest points is uniquely determined.
