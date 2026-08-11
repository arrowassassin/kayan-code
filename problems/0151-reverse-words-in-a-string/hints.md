## Hint 1

The output spec quietly does three jobs at once: reverse word order, collapse space runs, and trim the ends. If you tokenize first — extract just the words — all three collapse into "join the tokens backwards".

## Hint 2

In Python, `s.split()` with no argument already handles leading, trailing, and repeated spaces. That one-liner is a legitimate answer — but be ready to show the manual version. Try scanning the string **from the right**: skip spaces, then walk to the start of the word you landed on.

## Hint 3

Manual scan: with `i` starting at the end, loop — (1) decrement `i` past spaces; if `i < 0` stop; (2) walk `j` left from `i` until a space or the string start; (3) the slice `s[j+1 : i+1]` is the next output word; (4) set `i = j`. Join collected words with single spaces. The `+1`s in that slice are where the off-by-ones live.
