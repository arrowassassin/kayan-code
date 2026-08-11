## Hint 1

Every decoding consumes the string front to back, one or two digits at a time. Trying both options recursively is correct but exponential — yet the number of ways to finish depends only on *where you are* in the string, not on how you got there.

## Hint 2

Let `dp[i]` = ways to decode the prefix `s[:i]`. The last code of any decoding is either one digit (`s[i-1]`, valid if it's `1`-`9`) or two digits (`s[i-2:i]`, valid if it's `10`-`26`). Add the ways from the corresponding shorter prefixes — it's Fibonacci with validity guards.

## Hint 3

Base: `dp[0] = 1` (empty string, one way: decode nothing). Handle zeros with care — `'0'` contributes as a single digit *never*, and as a two-digit code only in `"10"`/`"20"`; `"30"`, `"00"` and a leading `'0'` kill every path. Only two previous values are read, so two rolling variables give O(1) space.
