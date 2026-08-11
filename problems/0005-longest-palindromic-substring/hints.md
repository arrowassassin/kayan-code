## Hint 1

Checking all O(n^2) substrings for palindromicity costs O(n^3) — too slow at n = 1000. Flip the viewpoint: instead of asking "is this substring a palindrome?", ask "what palindromes exist *around this center*?"

## Hint 2

Every palindrome has a center: a character (odd length) or a gap between two characters (even length). That's only `2n - 1` centers total, and from each one you can grow outward while the mirrored characters match — each center's expansion is independent.

## Hint 3

For each index `c`, expand twice — once from `(c, c)` for odd palindromes and once from `(c, c+1)` for even ones — keeping the best window seen. When a mismatch stops the loop, the last *valid* window is one step inside the pointers; getting that off-by-one right is most of the implementation. O(n^2) worst case, O(1) extra space.
