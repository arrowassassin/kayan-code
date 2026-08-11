# Find Median from Data Stream

Numbers arrive one at a time, and at any point you may be asked for the **median** of everything received so far — the middle value when the numbers are laid out in sorted order, or the average of the two middle values when the count is even.

Implement the class `MedianFinder`:

- `MedianFinder()` — create an empty container.
- `addNum(num)` — receive the next integer from the stream.
- `findMedian() -> float` — return the median of all integers added so far. Answers within `10^-6` of the true value are accepted.

Both operations should be efficient: an interviewer will expect `addNum` in O(log n) and `findMedian` in O(1).

## Example

```
MedianFinder mf = MedianFinder()
mf.addNum(1)       # stream: [1]
mf.addNum(2)       # stream: [1,2]
mf.findMedian()    # returns 1.5   (average of 1 and 2)
mf.addNum(3)       # stream: [1,2,3]
mf.findMedian()    # returns 2.0
```

## Constraints

- `-10^5 <= num <= 10^5`
- Up to `5 * 10^4` calls to `addNum` and `findMedian` combined
- `findMedian` is only called after at least one `addNum`
