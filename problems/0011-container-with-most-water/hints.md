## Hint 1

Checking every pair is O(n²) and the constraint is 10⁵. When the answer is over *pairs* and you need better than quadratic, ask: starting from some extreme configuration, which candidates can I rule out without looking at them?

## Hint 2

Start with the widest container: pointers at both ends. Any move inward shrinks the width — so a move is only worth it if it might raise the water level. Which of the two walls limits the water level, and what happens to *every* container that still uses that wall?

## Hint 3

The shorter wall caps the area: pairing it with any closer wall gives `<= min` the same cap and strictly less width. So the shorter wall can never appear in a better container — discard it and move that pointer inward, recording the area at each step. Ties: moving either pointer is fine.
