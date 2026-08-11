# Kth Largest Element in a Stream

Scores arrive over time, and after every new score you must report the **k-th largest value seen so far** (counting duplicates — this is the k-th element in sorted order, not the k-th *distinct* value). Implement `KthLargest`:

- `KthLargest(k, nums)` — initialize with the target rank `k` and an initial list of scores `nums` (possibly shorter than `k`).
- `add(val) -> int` — record a new score and return the current k-th largest.

It is guaranteed that at least `k` scores have been recorded whenever `add` returns.

## Example

```
KthLargest kl = KthLargest(3, [4, 5, 8, 2])
kl.add(3)    # returns 4    sorted so far: [8,5,4,3,2]
kl.add(5)    # returns 5    sorted so far: [8,5,5,4,3,2]
kl.add(10)   # returns 5    sorted so far: [10,8,5,5,4,3,2]
kl.add(9)    # returns 8
kl.add(4)    # returns 8
```

## Constraints

- `1 <= k <= 10^4`
- `0 <= len(nums) <= 10^4`
- `-10^4 <= nums[i], val <= 10^4`
- Up to `10^4` calls to `add`
- When `add` is called, the total number of recorded scores is at least `k`
