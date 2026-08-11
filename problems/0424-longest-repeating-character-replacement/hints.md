## Hint 1

Rephrase the goal: you want the longest window that can be turned into one repeated letter using at most `k` edits. "Longest window satisfying a budget" is a sliding-window shape — think about how to express the budget in terms of the window's letter counts.

## Hint 2

A window of length `L` whose most frequent letter appears `f` times needs exactly `L - f` replacements. So the window is valid iff `(window length) - (max letter count in window) <= k`. Maintain per-letter counts as the window moves.

## Hint 3

Keep `max_freq` as the highest count ever observed and never let the window shrink — when the window over-runs the budget, slide both ends forward together (evict one char, keep the length). A stale `max_freq` only makes the window *harder* to keep, never lets an invalid answer through, because the answer is the largest window size ever achieved — think about why that's safe, then return `len(s) - left`.
