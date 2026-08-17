# Capacity to Ship Packages Within D Days

A conveyor belt feeds packages onto a ship **in the given order** — `weights[i]` is the weight of the i-th package. Each day the ship is loaded with the next consecutive packages from the belt, up to its weight capacity, then departs; packages may never be reordered or split.

Return the **minimum** ship capacity that gets every package delivered within `days` days.

## Example 1

```
Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
```

With capacity 15 the daily loads are `[1,2,3,4,5] [6,7] [8] [9] [10]` — exactly 5 days. Capacity 14 would force `[1,2,3,4] [5,6] [7] [8] [9] [10]` = 6 days, one too many.

## Example 2

```
Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
```

Capacity 6 packs `[3,2] [2,4] [1,4]`. Note the belt order forbids grouping the two 4s together even though that might look tempting.

## Example 3

```
Input: weights = [1,2,3,1,1], days = 4
Output: 3
```

`[1,2] [3] [1] [1]`.

## Constraints

- `1 <= len(weights) <= 5 * 10^4`
- `1 <= weights[i] <= 500`
- `1 <= days <= len(weights)` (a valid capacity always exists)
- Packages must ship in belt order; a single package is never split across days.
