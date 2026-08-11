## Hint 1

Comparing the strings directly fails twice: `"1.2" < "1.10"` is false as strings (character `'2' > '1'`), and `"1.0"` vs `"1"` differ as text but not as versions. Both problems vanish if you compare **numeric chunks**, not characters.

## Hint 2

Split both strings on `'.'`. Now you have two lists of different lengths — instead of special-casing the leftover tail, imagine both lists padded with zeros to the same length. What loop bound expresses that?

## Hint 3

Loop `i` to `max(len(a), len(b))`; take `int(a[i])` if in range else `0`, same for `b`; return on the first inequality, `0` after the loop. `int()` absorbs the leading-zero rule for free — and note the first difference decides everything, so never keep comparing after it.
