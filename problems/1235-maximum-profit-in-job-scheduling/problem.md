# Maximum Profit in Job Scheduling

You are offered `n` jobs. Job `i` runs over the half-open time span `[startTime[i], endTime[i])` and pays `profit[i]` on completion. You can work on at most one job at any moment, but a new job may begin at the exact instant another one ends.

Choose a set of pairwise non-conflicting jobs that maximizes total profit, and return that maximum.

## Example 1

```
Input: startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
Output: 120
```

Take job 0 (`[1,3)`, pays 50) and job 3 (`[3,6)`, pays 70): they touch at time 3 but do not overlap. Total `50 + 70 = 120`.

## Example 2

```
Input: startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
Output: 150
```

Jobs 0 (`[1,3)`, 20), 3 (`[4,6)`, 70) and 4 (`[6,9)`, 60) fit together for 150. The 100-profit job blocks too much of the timeline to be worth it.

## Example 3

```
Input: startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
Output: 6
```

All three jobs overlap at time 1 — pick the single most profitable one.

## Constraints

- `1 <= n <= 5 * 10^4` where `n = len(startTime) = len(endTime) = len(profit)`
- `1 <= startTime[i] < endTime[i] <= 10^9`
- `1 <= profit[i] <= 10^4`

Times only bound each job (`start < end`); jobs arrive in no particular order and may duplicate each other. An O(n^2) approach will not pass the largest tests.
