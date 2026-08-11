# Longest Repeating Character Replacement — Editorial

## 1. Pattern recognition

Strip the story away and it reads: "longest contiguous window that satisfies a *budget*". A window of length `L` whose most common letter appears `f` times needs `L - f` edits to become uniform, so the condition is `L - max_freq <= k`. Budgeted-window conditions are monotone under shrinking (removing characters never increases `L - max_freq` beyond repair), which is the green light for the sliding-window template. What makes this problem famous is a subtlety layered on top: the window here is allowed to *never shrink* — the "cached max frequency" trick that trips up almost everyone the first time.

## 2. Brute force first

Try every window and count letters: O(n²) windows with incremental counts, O(26) validity check each → roughly O(26·n²). At n = 10⁵ that's ~2.6·10¹¹ — far past any time limit. As usual the waste is recomputation: adjacent windows share nearly all their counts, so maintain the counts once and move two pointers.

## 3. The key insight

**The answer only cares about the largest valid window ever achieved — so `max_freq` may go stale and the window may stay too big; neither can ever *overstate* the answer, only fail to shrink below it.**

## 4. Step-by-step derivation

1. Standard template first: expand `right`, keep 26 counts, and while `(right - left + 1) - max(counts) > k`, evict from the left. Recomputing `max(counts)` is O(26) per step — that already passes and is a perfectly good interview answer.
2. Now the refinement. Cache `max_freq` = the highest single-letter count *ever seen in any window*. When a character leaves the window we do **not** decrease it. Isn't that wrong? The window condition `L - max_freq <= k` becomes optimistic — it may hold windows that aren't currently valid.
3. Here's why it's safe: the final answer equals the *maximum window size that was ever valid*. A stale (too high) `max_freq` lets the window keep a length it once legitimately earned; it never lets the window *grow* unless `count[c]` genuinely pushes `max_freq` to a new record — and at that moment the window really is valid. So window length is a high-water mark: it never shrinks below the best answer, and it only rises on genuinely valid windows.
4. Consequently, replace the `while`-shrink with a single `if`-slide: when over budget, evict one char and advance `left` once — window length stays constant. The two pointers move in lockstep after the optimum is found.
5. The final window length `len(s) - left` *is* the answer — no per-step `best` tracking needed (keeping one anyway is fine and easier to defend under pressure).

## 5. Annotated Python solution

```python
from collections import Counter


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = Counter()
        max_freq = 0        # highest count EVER seen; deliberately never decreased
        left = 0
        for right, c in enumerate(s):
            count[c] += 1
            max_freq = max(max_freq, count[c])
            # over budget -> slide, don't shrink: length is a high-water mark
            if (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
        return len(s) - left
```

## 6. Complexity

- **Time O(n)** — "each pointer advances at most n times and every step is O(1); no 26-way scan needed thanks to the cached max."
- **Space O(1)** — "at most 26 counter entries regardless of n."

## 7. Edge-case traps

- **`k = 0`** — degenerates to longest existing run; the budget check must use strict `> k`.
- **`k >= len(s)`** — the whole string is achievable; the shrink branch never fires.
- **Single character string** → 1.
- **The stale-max worry itself** — interviewers *will* ask "your `max_freq` is wrong after eviction, why is the answer right?" Rehearse the high-water-mark argument from step 3; hand-waving here is the most common way to lose the problem after solving it.
- **Best window ends mid-string** (`"AABABBA", k=1`) — sliding (not shrinking) still preserves the earlier record length.

## 8. Reusable template

Not DP. This trains the *non-shrinking* maximization variant of the sliding window — window length as a monotone high-water mark — the same argument that speeds up Max Consecutive Ones III and any "longest window under an edit budget" problem.

## 9. Interviewer follow-up

- *"Lowercase + uppercase, or full unicode?"* — the algorithm is alphabet-agnostic; only the O(Σ) fallback of rescanning counts gets pricier, which is exactly why the cached-max version matters.
- *"Return the substring, not the length"* — you must track `(left, best_len)` at record time; the non-shrinking trick still works because records only happen when the window is genuinely valid.
- *"Replace with a specific letter only, say 'A'"* — the condition becomes `(# non-A in window) <= k`: this is Max Consecutive Ones III (1004) in disguise, a strictly simpler budget with the identical skeleton.
- *"What if edits had per-position costs?"* — the budget is now a sum; still monotone (all costs positive), so the window survives — but note that if 'costs' could be negative, monotonicity dies and you'd need prefix sums instead.
