# Longest Substring Without Repeating Characters — Editorial

## 1. Pattern recognition

"Longest **contiguous** substring satisfying a property" — the moment a problem asks for the best *window* in a linear sequence, and the property is one you can maintain incrementally (here: "all characters distinct"), reach for a **sliding window**. The tell is that the property is *monotone under shrinking*: if a window has all-distinct characters, so does every window inside it. That monotonicity is what makes "expand right, shrink left when broken" correct. This is the canonical entry point to the whole sliding-window family — nail it, and Minimum Window Substring (its linked follow-up) is the same skeleton with a richer invariant.

## 2. Brute force first

Check every substring: two nested loops for the endpoints, plus a set-build to test distinctness → O(n³), or O(n²) if you extend a set per start index. With n up to 5·10⁴, O(n²) is ~2.5·10⁹ character touches — dead at a 3-second limit, and an interviewer will ask you to do better before you finish writing it. The waste is obvious once you say it aloud: substrings starting at `left` and `left+1` share almost all their characters, and the brute force rediscovers that shared work every time.

## 3. The key insight

**When a window with distinct characters absorbs a duplicate of `c`, every window still containing the *old* `c` is invalid — so `left` can jump straight past the old occurrence.**

## 4. Step-by-step derivation

1. Maintain a window `[left, right]` that always satisfies the invariant "no repeats". Advance `right` one character per step.
2. Only the newly added `s[right]` can break the invariant. Naive repair: pop characters from the left until the duplicate is gone. That's already O(n) total — each index enters and leaves the window at most once — the amortized argument you should state explicitly in an interview.
3. Sharper repair: store `last[c]`, the most recent index of each character. If `last[s[right]]` is inside the window, no window containing that old index can ever be valid again, so set `left = last[s[right]] + 1` directly.
4. The guard `last[c] >= left` is load-bearing: a stale occurrence *before* the window must not drag `left` backwards. `"abba"` is the classic killer — at the final `'a'`, `last['a'] = 0` but `left` is already 2; moving left back to 1 would readmit the duplicate `'b'` and report 3 instead of 2.
5. Record `right - left + 1` after every extension; the max over all steps is the answer.

## 5. Annotated Python solution

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}          # char -> index of its most recent occurrence
        best = left = 0
        for right, c in enumerate(s):
            # duplicate is only a problem if it sits INSIDE the window;
            # the >= left guard stops left from moving backwards ("abba")
            if c in last and last[c] >= left:
                left = last[c] + 1
            last[c] = right
            best = max(best, right - left + 1)
        return best
```

## 6. Complexity

- **Time O(n)** — "one pass; `left` and `right` each only move forward, so every index is processed a constant number of times."
- **Space O(min(n, Σ))** — "the map holds at most one entry per distinct character in the alphabet."

## 7. Edge-case traps

- **`"abba"`** — the stale-occurrence trap from step 4; the single most common wrong answer here.
- **Empty string** → 0; the loop must simply not run.
- **All identical characters** (`"bbbbb"`) → 1; `left` chases `right` the whole way.
- **Answer at the very end** (`"dvdf"` → `"vdf"`, `"tmmzuxt"` → `"mzuxt"`) — updating `best` before repairing the window, or only at repair time, misses these.
- **Spaces/symbols are characters too** — don't assume 26 lowercase letters.

## 8. Reusable template

Not DP. This trains the core sliding-window template — expand `right` every step, repair `left` only when the invariant breaks, harvest the answer per step — the exact skeleton reused by Minimum Window Substring, Fruit Into Baskets, and Character Replacement.

## 9. Interviewer follow-up

- *"Now find the smallest window covering all characters of a second string"* — Minimum Window Substring (76), the linked extension: same two pointers, but the invariant flips from "no repeats" (shrink when broken) to "covers t" (shrink while satisfied), and you harvest minima during the shrink instead of maxima during the expand.
- *"Allow each character at most twice"* — replace the jump-map with counts and shrink while `count[c] > 2`; generalizes to at-most-k occurrences.
- *"What if the 'window' property were about a sum with negative numbers?"* — monotonicity dies, sliding window is no longer valid, and you pivot to prefix sums + hashing; saying this unprompted is a strong signal.
