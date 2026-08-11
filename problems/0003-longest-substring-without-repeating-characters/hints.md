## Hint 1

"Longest contiguous run satisfying a property" over a string is the signature of a **sliding window**: instead of re-checking every substring from scratch, maintain one window `[left, right]` and reuse the work as it moves.

## Hint 2

The window invariant is "all characters distinct". Grow `right` one step at a time; the invariant can only break because of the character you just added. What do you need to remember about the window's contents to detect and repair that break quickly?

## Hint 3

Keep a map from character to the index where you last saw it. When the new character `s[right]` was last seen **inside** the current window, jump `left` directly to `last[c] + 1` — don't shrink one step at a time, and don't move `left` backwards when the stale occurrence lies before the window (test on `"abba"`). Track the max window length as you go.
