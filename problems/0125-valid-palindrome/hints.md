## Hint 1

Two sub-problems are hiding in one statement: *which characters count*, and *is the surviving sequence symmetric*. You could solve them in two passes (build the cleaned string, then compare with its reverse) — that already works. Can you do it without building anything?

## Hint 2

Put one pointer at each end. The comparison only ever involves the next *counting* character from the left and the next counting character from the right — punctuation and spaces are just noise to step over.

## Hint 3

While `i < j`: advance `i` while `s[i]` is not alphanumeric, retreat `j` likewise, then compare `s[i].lower()` with `s[j].lower()`. Keep the `i < j` guard *inside* the skip loops too, or an all-punctuation string walks the pointers past each other.
