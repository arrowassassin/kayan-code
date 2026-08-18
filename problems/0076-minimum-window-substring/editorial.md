# Minimum Window Substring — Editorial

## 1. Pattern recognition

"**Shortest** contiguous substring **covering** a requirement" — two signals, one conclusion. Contiguous + linear input says two pointers over `s`; and the coverage property is *monotone under growing*: if a window covers `t`, every window containing it also covers `t`. Monotone properties are exactly what sliding windows exploit. This is a ★ top-priority problem and the capstone of the window family: it takes the skeleton from Longest Substring Without Repeating Characters (its linked warmup) and flips it — there the window property was "good until broken" and you maximized; here it's "bad until satisfied" and you minimize, harvesting *during the shrink phase* instead of the expand phase.

## 2. Brute force first

Try every window: O(n²) windows, each checked against `t`'s counts in O(window + |t|) → O(n³)-ish, or O(n² · 52) with per-start incremental counts. At n = 10⁵ even the n² variant is ~10¹⁰ operations — hopeless. The wasted work: windows `[l, r]` and `[l+1, r]` differ by one character, yet the brute force recounts everything. A sliding window pays for each character exactly twice — once entering, once leaving.

## 3. The key insight

**Coverage can be tracked with a single integer — `missing`, the number of still-required characters counting multiplicity — so validity checks are O(1) instead of a 52-key map scan.**

## 4. Step-by-step derivation

1. Build `need = Counter(t)`. A window covers `t` iff every `need` count is ≤ 0 after subtracting the window's characters. Checking all keys per step costs O(Σ) — fine, but the `missing` counter removes even that.
2. Let counts go **negative** for surplus copies; that's the multiplicity bookkeeping. `need[c] > 0` *before* decrementing means "this copy was still required" → `missing -= 1`. Symmetrically when a character leaves: `need[c] > 0` *after* incrementing means "we just gave up a required copy" → `missing += 1`. Counts only cross zero at those moments, which is why one integer stays in sync with 52 of them.
3. Standard two-phase loop: advance `right`, absorbing `s[right]`. While `missing == 0`, the window is valid — record `(left, length)` if it's the shortest so far, then evict `s[left]` and advance `left`. The shrink loop exits the instant validity breaks, so you always record the *tightest* window for each `right`.
4. Why harvest inside the shrink loop? Because for a minimization problem, a valid window is only interesting once it can't shrink further; expanding a valid window never helps. This phase inversion relative to problem 3 is the whole lesson.
5. Return the recorded slice — track `(best_left, best_len)`, never build substrings in the loop (slicing per step degrades to O(n²)).

## 5. Annotated Python solution

```python
from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(t) > len(s):
            return ""

        need = Counter(t)          # >0: still required; <=0: satisfied/surplus
        missing = len(t)           # required chars outstanding, WITH multiplicity
        best_len = float("inf")
        best_left = 0
        left = 0

        for right, c in enumerate(s):
            if need[c] > 0:        # this copy was still needed
                missing -= 1
            need[c] -= 1           # negative = surplus, and that's fine

            while missing == 0:    # valid -> harvest at the TIGHTEST point
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_left = left
                lc = s[left]
                need[lc] += 1
                if need[lc] > 0:   # just surrendered a required copy
                    missing += 1
                left += 1

        return "" if best_len == float("inf") else s[best_left:best_left + best_len]
```

## 6. Complexity

- **Time O(|s| + |t|)** — "each pointer only moves forward, so every character of `s` enters the window once and leaves at most once; all per-step work is O(1)."
- **Space O(Σ)** — "the counter holds at most one entry per distinct character — effectively O(1) for a fixed alphabet."

## 7. Edge-case traps

- **Multiplicity**: `t = "ABCC"` demands two `'C'`s. Solutions that track a *set* of needed characters, or cap counts at zero incorrectly, pass `"ABC"`-style tests and fail here.
- **`t` longer than `s`** → `""` immediately.
- **No valid window at all** (`t` has a character absent from `s`) — `missing` never hits 0; make sure you return `""`, not a stale slice.
- **Whole string is the answer** (`s = "abc"`, `t = "cba"`).
- **Duplicates in `t` equal to duplicates in `s`** (`s = "aa"`, `t = "aa"`) — the shrink loop must not over-evict.
- **Case sensitivity** — `'A'` ≠ `'a'`.

## 8. Reusable template

Not DP. This trains the *minimization* variant of the sliding-window template — expand until valid, then shrink-and-harvest while valid — plus the `missing`-counter trick for O(1) validity, reused anywhere a window must "cover" a multiset.

## 9. Interviewer follow-up

- *"Stream `s` and can't store it?"* — you must remember candidate window contents; discuss keeping only counts plus the current window in a bounded buffer, and why the exact substring answer needs O(window) memory no matter what.
- *"Return all minimal windows / count them"* — same loop; every time the shrink loop reaches its tightest valid point you have one candidate per `right`; collect matches of the best length in a second pass.
- *"Window must contain the characters of `t` in order?"* — coverage is no longer a counting property; sliding window dies, and it becomes Minimum Window Subsequence — two-pointer forward/backward passes or DP. Recognizing *when the window breaks* is the interviewer probe here.
