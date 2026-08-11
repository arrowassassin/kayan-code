## Hint 1

Rewrite `5-9/2*3+8` in your head as a **sum of terms**: `5`, `-(9/2*3)`, `+8`. Addition and subtraction only ever separate terms; multiplication and division happen *inside* a term. If you can collect the terms, the answer is just their sum.

## Hint 2

Scan once, keeping the number currently being read and the **last unresolved operator**. When you hit the next operator (or the end of the string): if the pending op is `+`/`-`, push `±num` onto a stack of finished terms; if it is `*` or `/`, the new number combines with the **top of the stack** — pop, apply, push back.

## Hint 3

Two Python traps: (1) the last number has no operator after it, so also flush when you reach the final character; (2) `//` floors, but the spec truncates toward zero — use `int(a / b)` (or trim spaces carefully and quotient logic). Check yourself on `"0-3/2"`: the answer is `-1`.
