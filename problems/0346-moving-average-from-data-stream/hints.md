## Hint 1

Recomputing the average by summing the whole window on every call works, but it repeats work: between two consecutive calls, the window barely changes. What exactly changes when one value arrives?

## Hint 2

Exactly one value enters the window, and (once the window is full) exactly one value leaves — the oldest. If you maintain a **running sum**, each `next` is one addition, maybe one subtraction, and one division. The only question left is how to find "the oldest value" in O(1).

## Hint 3

Keep the window in a `deque` (or a fixed-size ring buffer with a write index). Append the new value and add it to the sum; if the deque is now longer than `size`, `popleft()` the oldest and subtract it. Return `sum / len(window)` — dividing by the current length handles the warm-up phase before the window fills.
