## Hint 1

Forget the array for a second and ask a purely local question: at one single position `i`, how high does the water surface stand? It depends on exactly two quantities about the rest of the array.

## Hint 2

The water level above position `i` is `min(tallest to the left of i, tallest to the right of i)`, and the water held there is that level minus `height[i]` (never negative). Two prefix/suffix maximum arrays make this an easy O(n) time / O(n) space solution — get that working first.

## Hint 3

To drop the arrays: walk pointers inward from both ends, maintaining `max_left` and `max_right` seen so far. When `max_left <= max_right`, the true water level at the left pointer is already determined — the right side is guaranteed to hold at least `max_left` — so you can settle that cell immediately and advance. Mirror for the other side.
