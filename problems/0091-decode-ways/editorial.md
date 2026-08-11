# Decode Ways — Editorial

## 1. Pattern recognition

"How many ways can this string be segmented into valid pieces?" — the counting sibling of Word Break (139, this problem's warmup). There the pieces came from a dictionary and the question was *whether* a split exists (an OR over choices); here the "dictionary" is the codes 1–26 and the question is *how many* splits exist (a SUM over choices). Same prefix-DP skeleton, different combiner. Because every code is 1 or 2 digits, the recurrence only reaches back two positions — structurally Fibonacci, wearing validity guards. The real difficulty is not the DP; it's the `'0'` bookkeeping.

## 2. Brute force first

Recursively peel one or two digits off the front and recurse on the rest. Branching factor 2, depth up to 100 → O(2^n) paths; `"1"×100` alone has ~5.7 × 10^20 decodings, and the naive recursion walks every one. But each call is identified purely by its start position — 101 distinct subproblems. As always, the exponential cost is re-answering the same suffix over and over; memoize and it's linear.

## 3. The key insight

**Every decoding ends with a final code of one or two digits, so `dp[i] = dp[i-1]·[s[i-1] valid alone] + dp[i-2]·[s[i-2:i] in 10..26]` — Fibonacci with guards, and zeros are handled entirely by the guards.**

## 4. Step-by-step derivation

1. **Name the state.** `ways(i)` = number of decodings of the prefix `s[:i]`. The letters already produced don't influence how the rest can be decoded — position is a complete summary.
2. **Say the choice out loud** — for counting, the "choice" is the last code: "any decoding of `s[:i]` ends with either a 1-digit code `s[i-1]` or a 2-digit code `s[i-2:i]`. The two cases are disjoint (different last-code lengths) and exhaustive, so I *add* the counts of the shorter prefixes — when the codes are valid."
3. **Encode validity, i.e. the zero traps:**
   - 1-digit code: valid iff `s[i-1] != '0'` — nothing maps to 0.
   - 2-digit code: valid iff `10 <= int(s[i-2:i]) <= 26` — this window is what lets `'0'` survive, and only after a 1 or 2. (String comparison `"10" <= t <= "26"` works too since both sides are 2 chars.)
4. **Base case:** `ways(0) = 1` — the empty string decodes in exactly one way (produce nothing). This 1, not 0, is what makes the two-digit branch count correctly on inputs like `"12"`.
5. **Memoize:** 2^n call tree → n+1 cached positions, O(1) each → O(n). The `"11111..."` stress case collapses from 10^20 walks to 100 additions producing the exact big-integer count.
6. **Compress:** only `dp[i-1]` and `dp[i-2]` are read — two rolling variables, exactly like House Robber and Fibonacci.

## 5. Annotated Python solution

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        # two_back = ways(s[:i-1]), one_back = ways(s[:i])
        two_back, one_back = 1, 1 if s[0] != "0" else 0   # ways(""), ways(s[:1])
        for i in range(1, len(s)):
            cur = 0
            if s[i] != "0":                       # last code = single digit 1-9
                cur += one_back
            if "10" <= s[i - 1 : i + 1] <= "26":  # last code = two digits
                cur += two_back
            two_back, one_back = one_back, cur    # slide the window
        return one_back
```

Note there is no special "return 0" for dead strings: a position with no valid last code gets `cur = 0`, and that zero propagates — the guards *are* the zero handling.

## 6. Complexity

- **Time O(n)** — "one constant-time check per position; each prefix is counted exactly once."
- **Space O(1)** — "the recurrence reaches back only two positions, so two rolling variables replace the table."

## 7. Edge-case traps

- **Leading `'0'`** (`"06"`, `"0"`) → 0 immediately; the init `1 if s[0] != '0' else 0` covers it.
- **`"10"` → 1, `"100"` → 0** — the second `0` has no `1`/`2` in front to attach to. Trailing zeros are where hand-waved solutions die.
- **`"27"` → 1** — two-digit codes stop at 26; `>= 27` splits are single-digit only. Checking `s[i-1] in "12"` without checking the second digit's range wrongly accepts `"27"` as a pair.
- **`"00"`, `"30"`** → 0 — a zero preceded by the wrong digit poisons every path.
- **`"2101"` → 1** — zeros *force* pairings and can make the count collapse to exactly one; nice mid-string trap.
- **Huge counts** (`"1"×100` ≈ 5.7 × 10^20) — exceeds 64-bit signed range; Python is exact, in other languages mention overflow or a modulus.

## 8. Top-down AND bottom-up (+ the conversion recipe)

**Top-down (memoized recursion)** — peel codes off the front:

```python
from functools import lru_cache

class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        @lru_cache(maxsize=None)
        def ways(i: int) -> int:              # decodings of the suffix s[i:]
            if i == n:
                return 1                      # base: consumed everything - one way
            if s[i] == "0":
                return 0                      # base: a code can't start with 0
            total = ways(i + 1)               # take one digit
            if i + 2 <= n and "10" <= s[i:i + 2] <= "26":
                total += ways(i + 2)          # take two digits
            return total

        return ways(0)
```

**Bottom-up (iterative table)** — same recurrence on prefixes; section 5 is this with the table compressed:

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1                             # init = base case: empty string
        for i in range(1, n + 1):             # loop order: shorter prefixes first
            if s[i - 1] != "0":
                dp[i] += dp[i - 1]
            if i >= 2 and "10" <= s[i - 2:i] <= "26":
                dp[i] += dp[i - 2]
        return dp[n]
```

**The mechanical conversion recipe:**

1. **State → params → table index.** The memo key `i` (a position) becomes the array index `dp[i]`.
2. **Memo → table.** `@lru_cache` becomes `dp = [0] * (n + 1)` — one slot per position, including the empty-prefix slot.
3. **Recursion order → loop order.** The top-down version recurses on *larger* `i` (suffixes); mirrored to prefixes, dependencies point at *smaller* `i`, so the loop ascends `1 .. n` — `dp[i-1]` and `dp[i-2]` are final when read.
4. **Base case → initialization.** `if i == n: return 1` becomes `dp[0] = 1`; the "invalid path" zeros need no code at all — they're the table's default fill.

Final pass: two-back dependency → two rolling variables (section 5).

## 9. Interviewer follow-up

- **Add `'*'` wildcards** (Decode Ways II, 639): a `'*'` means any digit 1–9. Same two-branch recurrence, but each guard becomes a *count multiplier* (e.g. `'*'` alone contributes 9·dp[i-1]; `"1*"` contributes 9 two-digit ways, `"2*"` six) — usually with answers mod 10^9+7. Deriving the multiplier table live is the whole exercise.
- **Return one valid decoding / all decodings:** switch from counts to backtracking with the same validity guards; note the output can be exponential, so ask which is wanted.
- **Arbitrary code dictionary instead of 1–26?** That is literally Word Break (139) for existence and its counting variant for this problem — the bridge back to the warmup: dictionary lookups replace the `10..26` guard, and the look-back extends from 2 to the longest word.
