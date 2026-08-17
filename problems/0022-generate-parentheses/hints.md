## Hint 1

Building all `2^(2n)` strings of `(` and `)` and filtering the balanced ones works but drowns in garbage — for n = 8 only 1,430 of 65,536 strings survive. Instead, build the string one character at a time and ask: at each position, when is it *legal* to place `(`, and when `)`?

## Hint 2

Track two counters as you build: `opened` and `closed`, the number of each bracket placed so far. You may place `(` whenever `opened < n` (you still have opens left), and `)` only when `closed < opened` (there's an unmatched `(` for it to close). Convince yourself these two rules are exactly the definition of a well-formed prefix.

## Hint 3

Recurse with the shared partial string and the two counters: try `(` (if legal), recurse, undo; try `)` (if legal), recurse, undo. When the length hits `2n`, the string is complete *and automatically valid* — the rules never let an invalid prefix exist, so there is no final validation step. Every recursion path emits a distinct valid string: enumeration without filtering.
