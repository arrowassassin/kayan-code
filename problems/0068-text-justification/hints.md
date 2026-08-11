## Hint 1

Split the problem into two completely separate phases: **packing** (which words share a line?) and **rendering** (how are the spaces laid out?). Mixing them is what makes this problem feel hard. Packing is greedy: `k` words fit if their total length plus `k-1` (minimum one space per gap) is at most `maxWidth`.

## Hint 2

For rendering a full line with `g` gaps and `S` leftover spaces (width minus total word length): every gap gets `S // g` spaces, and the first `S % g` gaps get one extra. Compute both with a single `divmod`.

## Hint 3

Two cases refuse the even-spread rule: a line with exactly **one** word, and the **final** line — both are left-justified and padded on the right. Notice they can be handled by the same branch (`j == n or count == 1`). Off-by-one check: the extra-space test is `gap_index < remainder`, and padding is `maxWidth - len(line)`, never assumed zero.
