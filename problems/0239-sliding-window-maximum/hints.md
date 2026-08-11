## Hint 1

Recomputing `max` over each window costs O(k) per slide — O(nk) overall, which the stress test punishes. The windows overlap in `k - 1` elements; the question is what summary of the current window lets you answer "max?" in O(1) *and* stays cheap to update when one element enters and one leaves.

## Hint 2

When a new element `x` enters, every element already in the window that is `<= x` can **never** be a future window's maximum — `x` is at least as large and will outlive them all. Discard them permanently. What order do the survivors end up in?

## Hint 3

Keep a deque of **indices** whose values are strictly decreasing front to back. On each step: pop from the back while the back's value is `<= x`, push `x`'s index, pop the front if its index has slid out of the window (`dq[0] <= i - k`), and once the first window is complete, read the answer at the front. Store indices, not values — you can't tell when a value expires otherwise.
