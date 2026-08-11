# Valid Number — Editorial

## 1. Pattern recognition

The statement is not an algorithm problem — it's a **grammar**, delivered in prose. Whenever a validity question comes with a pile of "optional this, then maybe that" rules, the winning move is to transcribe the rules into a formal shape *before* coding:

```
number   := space* sign? core exponent? space*
core     := digits | digits '.' | digits '.' digits | '.' digits
exponent := ('e'|'E') sign? digits
```

That's a regular language, so three implementations exist: a regex, a DFA table, or **structured sequential parsing** (a hand-rolled recursive-descent for a non-recursive grammar). This problem is Hard purely because of edge-case density — every ambiguous English sentence in the spec is a hidden test. The interview habit it trains is the one that transfers everywhere: read the spec out loud, enumerate the token classes, and write down which parts may be empty. Do that and `"3."` vs `"."` vs `".e1"` stop being surprises and become rows in your table.

## 2. Brute force first

The tempting shortcuts:

- `float(s)` in a try/except — rejected by interviewers, and also *wrong*: Python accepts `"inf"`, `"nan"`, `"1_000"`, none of which the grammar allows.
- A pile of counters (`count('.') <= 1`, `count('e') <= 1`, ...) — counting can't express *ordering* (`".e1"` has legal counts but digits are required before `e`), so this route decays into patch-on-patch.
- A regex like `^ *[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)? *$` — genuinely correct and the pragmatic answer in production Python; say so, then add that the interviewer wants the parser because a regex proves you can *transcribe* a grammar, not that you can *implement* one — and the sequential parser is what scales to grammars regex can't do (nesting).

## 3. The key insight

**Consume the string left to right in grammar order — sign, digits, dot, digits, e, sign, digits — tracking just two facts: "the core saw at least one digit" and "the exponent saw at least one digit"; accept iff both required facts hold and the input is fully consumed.**

## 4. Step-by-step derivation

1. Handle the spaces rule first: leading/trailing spaces are legal, interior ones are not. `strip(' ')` implements exactly that, because any *interior* space will later fail the "fully consumed" check (`"1 2"` strips to `"1 2"`, and parsing halts at the space). One call, rule done.
2. Write one helper, `scan_digits(i) -> (new_i, moved)`. The grammar uses "one or more digits" three times; a shared helper means the off-by-ones live in one place. Compare `'0' <= c <= '9'` — `str.isdigit()` accepts `'٣'` and friends, a real-world unicode leak.
3. Parse the core: optional sign, digits, optional `.`, digits. Neither digit run is individually required — but their disjunction is: `int_digits or frac_digits`. This single boolean encodes four grammar shapes and kills `"."`, `"+"`, `"+."`, `""` in one line while admitting `"3."` and `".9"`.
4. Parse the exponent only if an `e`/`E` is present: optional sign, then digits that are **mandatory** (`exp_digits`). This kills `"1e"` and `"4e+"`. Note `"e9"` never even reaches this step — with no digit and no dot before the `e`, the core check in step 3 already rejected it; tracing *which* check fires for each bad input is a great five-minute self-review.
5. Accept iff `i == n`. This is the catch-all that rejects `"95a54e53"`, `"4.e2e3"` (second `e` unparsed), `"6+1"`, `"3-2"` — every "trailing garbage" case, with zero garbage-specific code. Structured parsing's superpower: *what you don't consume convicts the input.*

## 5. Annotated Python solution

```python
class Solution:
    def isNumber(self, s: str) -> bool:
        s = s.strip(" ")            # leading/trailing spaces are allowed, nothing else
        n = len(s)

        def scan_digits(i: int):
            """Advance past ASCII digits; report whether we saw at least one."""
            start = i
            while i < n and "0" <= s[i] <= "9":
                i += 1
            return i, i > start

        i = 0
        if i < n and s[i] in "+-":               # optional sign
            i += 1
        i, int_digits = scan_digits(i)           # integer part
        frac_digits = False
        if i < n and s[i] == ".":                # optional decimal point
            i += 1
            i, frac_digits = scan_digits(i)      # fractional part
        if not (int_digits or frac_digits):      # ".", "+", "+." all die here
            return False
        if i < n and s[i] in "eE":               # optional exponent
            i += 1
            if i < n and s[i] in "+-":
                i += 1
            i, exp_digits = scan_digits(i)
            if not exp_digits:                   # "4e", "4e+" die here
                return False
        return i == n                            # every character must be consumed
```

## 6. Complexity

- **Time O(n)** — "one forward pass; every character is examined exactly once by exactly one scan."
- **Space O(1)** — "an index and two booleans."

## 7. Edge-case traps

The hidden suite is built from the grammar's boundary rows:

- **Digits required *somewhere* in the core**: `"."`, `"+"`, `""`, `"  "` → false; `"3."`, `".9"`, `"+.8"` → true.
- **Digits required *after* `e`**: `"1e"`, `"4e+"` → false; `"2e10"`, `"2.e-7"`, `"1E5"` → true.
- **Order matters, not counts**: `".e1"` → false (no core digit before `e`); `"e9"` → false.
- **Trailing garbage**: `"95a54e53"`, `"4.e2e3"`, `"3-2"`, `". 1"` → false — all caught only by the final `i == n`.
- **Double signs**: `"--6"`, `"+-3"` → false; the sign is consumed at most once per position in the grammar.
- **Leading zeros are fine**: `"0089"`, `"-090"` → true — numbers, not integer literals.
- **Spaces**: allowed around (`" 0.1 "` → true), fatal inside (`"1 2"` → false).
- **Words**: `"Infinity"`, `"NaN"` → false — the `float()` shortcut's downfall.

## 8. (DP section — not applicable)

Not DP. This trains the **grammar-transcription parser** — index-passing `scan_*` helpers plus a final full-consumption check — the template for every validate-a-format question (dates, IPs, floats, semver).

## 9. Interviewer follow-up

- *"Draw it as a DFA"* — states {start, sign, int, dot-with-int, dot-without-int, frac, e, e-sign, exp}, accepting {int, dot-with-int, frac, exp}; the sequential parser *is* this automaton with states flattened into code position. Being able to translate between the two representations is the senior move.
- *"Add hex (`0x1A`) or underscores (`1_000`)"* — new alternatives in the grammar file, new branch in the parser; the regex meanwhile gets unreadable. This is the maintainability argument for structured parsing.
- *"Return the parsed value, not just validity"* — the parser already knows where each part starts and ends; accumulate during the same scan. A validator that can't be upgraded to a parser was written wrong.
- *"Why not `try: float(s)`?"* — enumerate the exact disagreements (`inf`, `nan`, `1_000`, unicode digits, `"1d2"` in some locales' C parsers) — knowing *where* the shortcut diverges from the spec is worth more than avoiding it on principle.
