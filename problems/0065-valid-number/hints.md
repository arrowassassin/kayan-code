## Hint 1

Don't start writing `if`s — start by transcribing the grammar. Read the spec out loud and list the token classes in order: spaces, sign, integer digits, dot, fraction digits, `e`/`E`, sign, exponent digits. Every one is optional *except* certain combinations — nail down exactly which parts must be non-empty.

## Hint 2

The two "at least one digit" rules carry the whole problem: (1) the decimal core needs digits **somewhere** — before the dot, after it, or both (`"3."`, `".9"` valid; `"."`, `"+"` invalid); (2) an exponent, once its `e` appears, needs digits **after** it (`"1e"`, `"4e+"` invalid). Track two booleans: `saw_core_digit`, `saw_exp_digit`.

## Hint 3

Write a helper `scan_digits(i)` returning the new index and whether it moved, then consume the string left to right: strip spaces, optional sign, digits, optional `.` + digits, check the core; optional `e` + sign + digits, check the exponent; finally **require `i == len(s)`** — leftover characters like the `a` in `"95a54e53"` must fail. Compare characters with `'0' <= c <= '9'`, not `str.isdigit()` (which accepts Unicode digits).
