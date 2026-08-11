# Longest Palindromic Substring — Editorial

## 1. Pattern recognition

"Longest substring with a symmetric property" sits at the crossroads of two techniques, and interviewers accept either: **expand around center** (the pragmatic favorite — palindromes are defined by their centers) and **interval DP** (the systematic one — `is_pal(i, j)` reduces to `is_pal(i+1, j-1)`). The tells: the property is checkable from the outside in, ties are allowed ("return any"), and n ≤ 1000 says O(n²) is the bar. Knowing *both* routes — and saying why you'd code the first — is the strong-candidate move.

## 2. Brute force first

Enumerate all O(n²) substrings, longest first, and test each for palindromicity in O(length): O(n³) overall, ~10^9 character comparisons at n = 1000 — over budget. The waste is blatant: testing `"abcba"` re-compares the inner `"bcb"` that a previous test already verified. Both real solutions are just two different ways of never re-verifying an inner palindrome.

## 3. The key insight

**Every palindrome is grown from one of only `2n − 1` centers (a character, or a gap between two characters) — expand each center outward while the mirrored characters match, and the longest expansion wins.**

## 4. Step-by-step derivation

1. **Reverse the question.** Instead of "is this substring a palindrome?" ask "how far does the palindrome *around this center* reach?" A palindrome's identity is its center plus a radius.
2. **Count the centers.** Odd-length palindromes center on a character (n of them); even-length ones center on a gap (`n − 1`). Miss the gaps and `"cbbd"` breaks — the classic bug.
3. **Expansion is safe and complete.** From center outward, characters must match pairwise; the first mismatch is final for that center (a longer palindrome on the same center would contain the mismatched pair). So one linear expansion per center finds *the* longest palindrome at that center — no backtracking.
4. **Complexity:** `2n − 1` centers × O(n) worst-case expansion = O(n²) time, O(1) space, and in practice most expansions die after a step or two — typically far faster than the DP table, which always does all O(n²) cells and stores them.
5. **The DP alternative** (section 8) makes the substructure explicit: `s[i..j]` is a palindrome iff `s[i] == s[j]` and `s[i+1..j-1]` is. It fills an O(n²) boolean table in increasing length order. Same asymptotics, O(n²) memory — but it *generalizes* (count palindromic substrings, minimum palindrome partitioning), which is why it's worth carrying in your head even when you code the expander.

## 5. Annotated Python solution

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        best_lo, best_hi = 0, 1                  # best window [lo, hi)

        def expand(lo: int, hi: int) -> None:
            nonlocal best_lo, best_hi
            # grow while in bounds and the mirror characters agree
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1
                hi += 1
            # loop overshoots by one step; the valid window is (lo, hi) exclusive
            if hi - lo - 1 > best_hi - best_lo:
                best_lo, best_hi = lo + 1, hi

        for c in range(len(s)):
            expand(c, c)                         # odd length: center at c
            expand(c, c + 1)                     # even length: center in the gap
        return s[best_lo:best_hi]
```

## 6. Complexity

- **Time O(n²)** worst case — "2n − 1 centers, each expanding at most n/2 steps"; inputs like `"aaaa..."` hit the bound, random text is near-linear.
- **Space O(1)** — "two indices for the best window; no table." (DP table version: O(n²) space.)

## 7. Edge-case traps

- **Even-length palindromes** (`"cbbd"` → `"bb"`, `"abba"`): forgetting the gap centers is the most common wrong submission.
- **Single character / no repeats** (`"ac"`) — the answer is any 1-char substring; initialize the best window to length 1, not 0.
- **Whole string is a palindrome** (`"abba"`, `"Aa9aA"`) — expansion must run to the walls; check the bounds test comes *before* the character test.
- **The off-by-one at mismatch:** when the while-loop stops, `lo`/`hi` sit one step *outside* the palindrome — the answer is `s[lo+1:hi]`. Most bugs in this problem are exactly here.
- **Case sensitivity** — `"Aa"` is not a palindrome; don't casefold.
- **Ties** — any maximum-length answer is accepted (the judge checks substring-of-input, palindromicity, and optimal length), so don't burn time matching a particular expected string.

## 8. Top-down AND bottom-up (+ the mechanical conversion recipe)

The DP formulation: `pal(i, j)` = "is `s[i..j]` (inclusive) a palindrome?" — recurrence `pal(i, j) = (s[i] == s[j]) and pal(i+1, j-1)`.

**Top-down (memoized recursion):**

```python
from functools import lru_cache

class Solution:
    def longestPalindrome(self, s: str) -> str:
        @lru_cache(maxsize=None)
        def pal(i: int, j: int) -> bool:      # is s[i..j] a palindrome?
            if i >= j:
                return True                   # base: empty or single char
            return s[i] == s[j] and pal(i + 1, j - 1)

        best = (0, 0)                         # (lo, hi) inclusive
        for i in range(len(s)):
            for j in range(i, len(s)):
                if j - i > best[1] - best[0] and pal(i, j):
                    best = (i, j)
        return s[best[0]:best[1] + 1]
```

**Bottom-up (iterative table)** — fill by increasing substring length so inner intervals exist first:

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[False] * n for _ in range(n)]  # dp[i][j] = s[i..j] is a palindrome
        best_lo, best_len = 0, 1
        for i in range(n):
            dp[i][i] = True                   # init = base case: length 1
        for length in range(2, n + 1):        # loop order: shorter intervals first
            for i in range(n - length + 1):
                j = i + length - 1
                # inner interval is length-2 (or empty): already filled
                dp[i][j] = s[i] == s[j] and (length == 2 or dp[i + 1][j - 1])
                if dp[i][j] and length > best_len:
                    best_lo, best_len = i, length
        return s[best_lo:best_lo + best_len]
```

**The mechanical conversion recipe:**

1. **State → params → table index.** The memo key `(i, j)` becomes the 2-D index `dp[i][j]`.
2. **Memo → table.** `@lru_cache` becomes an n × n boolean grid — one cell per interval.
3. **Recursion order → loop order.** `pal(i, j)` depends on the *shorter* interval `(i+1, j-1)`, so the loop iterates by increasing `length` — every inner interval is final before the outer one asks. (Interval DP always orders by length; contrast with the index-ascending order of prefix DPs.)
4. **Base case → initialization.** `i >= j → True` becomes the pre-set diagonal (length 1) and the `length == 2` short-circuit standing in for the empty interval.

Note what the DP buys and costs: identical O(n²) time (but always the *full* n²), O(n²) memory the expander doesn't pay — and a reusable table that follow-up problems query directly.

## 9. Interviewer follow-up

- **"Count all palindromic substrings"** (647): the expander counts every successful step instead of tracking a max; the DP counts true cells. Both are one-line edits — a great test of whether you understood the structure.
- **"Minimum cuts to partition into palindromes"** (132): the `dp[i][j]` table becomes the oracle for a second, 1-D DP over cut positions — the canonical payoff for having the systematic version.
- **"Can you beat O(n²)?"** — yes: **Manacher's algorithm** reuses mirrored information across centers for O(n); name it, sketch the mirror trick, and say you wouldn't code it live. Suffix-automaton/hashing + binary search (O(n log n)) is a middle road.
- **"Longest palindromic *subsequence*?"** (516) — drop contiguity and the interval DP shifts from booleans to lengths: `dp[i][j] = dp[i+1][j-1] + 2` on match, else `max` of dropping either end. The expander has no analogue — which is exactly why the DP view was worth keeping.
