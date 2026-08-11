# Text Justification — Editorial

## 1. Pattern recognition

No clever data structure, no asymptotic trick — this is a **pure specification-implementation** problem, and that's exactly why it's rated Hard: the difficulty is fidelity, not insight. The give-away structure is a pipeline: *pack* words into lines greedily, then *render* each line by one of three spacing policies. The interview habit that wins here is reading the spec out loud and enumerating the cases before typing: (a) full line with 2+ words, (b) line with exactly 1 word, (c) last line. Three render policies, one packing rule — writing that list down first turns a rat's nest into two small functions.

## 2. Brute force first

There's no complexity cliff (n ≤ 300; everything is O(total characters)) — the "brute force" failure mode is *structural*: interleaving packing and rendering in one loop, appending spaces while deciding whether the next word fits. That version accumulates flags (`is_first_word`, `pending_spaces`, `line_so_far`) and every edge case needs another flag. The disciplined version keeps a **pure packing loop** that computes only indices `[i, j)` and a word-length sum — no strings at all — and hands those to a renderer. Same big-O, wildly different bug surface.

## 3. The key insight

**Pack by indices greedily — `k` words fit iff `sum(lengths) + (k-1) <= maxWidth` — then render each line with `q, r = divmod(leftover_spaces, gaps)`: every gap gets `q` spaces and the leftmost `r` gaps get one more.**

## 4. Step-by-step derivation

1. Packing: starting at `i`, extend `j` while `length + len(words[j]) + (j - i) <= maxWidth`. The `(j - i)` term *is* the minimum one-space-per-gap requirement — folding it into the inequality avoids a separate "+1 unless first word" branch, a classic off-by-one nest.
2. Rendering a full line: `leftover = maxWidth - length` spaces spread over `gaps = count - 1`. `divmod(leftover, gaps)` gives the base gap `q` and the number `r` of gaps owed one extra. "Leftmost gaps get the extra" translates to: gap index `< r` → width `q+1`, else `q`. Gap sizes then differ by at most one and decrease left to right — the spec sentence, transcribed.
3. Two cases make `gaps = 0` or forbid spreading: a single word on the line (division by zero if you don't branch) and the last line (spec says left-justify). Both render identically — words joined by single spaces, padded right to `maxWidth` — so one branch, `j == n or count == 1`, covers both. Collapsing these two spec cases into one code path is the elegance point of the problem.
4. Every emitted line must be *exactly* `maxWidth` — including the padded last line and single-word lines. The final `+ " " * (maxWidth - len(line))` is not optional polish; tests measure line length.
5. Advance `i = j`, repeat. Each word is examined once by packing and written once by rendering.

## 5. Annotated Python solution

```python
class Solution:
    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        lines = []
        i, n = 0, len(words)
        while i < n:
            # greedily take words while they fit with 1 space between each
            j, length = i, 0
            while j < n and length + len(words[j]) + (j - i) <= maxWidth:
                length += len(words[j])
                j += 1
            count = j - i
            if j == n or count == 1:
                # last line, or a single word: left-justify, pad right
                line = " ".join(words[i:j])
                line += " " * (maxWidth - len(line))
            else:
                spaces = maxWidth - length
                q, r = divmod(spaces, count - 1)     # left gaps get the extra space
                parts = []
                for k in range(i, j - 1):
                    parts.append(words[k])
                    parts.append(" " * (q + (1 if k - i < r else 0)))
                parts.append(words[j - 1])
                line = "".join(parts)
            lines.append(line)
            i = j
        return lines
```

## 6. Complexity

- **Time O(total characters)** — "each word is scanned once during packing and copied once during rendering; space runs are built directly at their final size."
- **Space O(maxWidth)** beyond the output — "one line buffer at a time; the output itself is the required result."

## 7. Edge-case traps

- **A long word alone on a full (non-last) line** (`"acknowledgment"`) — must be left-justified with right padding, not crash on zero gaps.
- **The last line** — exactly one space between words plus right padding; accidentally justify-spreading it is the most common WA.
- **Uneven gap distribution** — `"This    is    an"`: leftmost gaps get the extra; `k - i < r`, not `<=`, and not rightmost.
- **A word exactly `maxWidth` wide** (`"exactfit"`, width 8) — fits alone with zero padding; the padding expression must tolerate zero.
- **Every line exactly `maxWidth`** — including single-word and last lines; length assertions catch half the bugs here.
- **Two words that exactly fill the width** (`"equal width"`, 11) — leftover 0, all gaps `q=1`, `r=0`; the divmod path must survive it.
- **Last line that is also full** — the `j == n` branch still left-justifies; the spec says the last line is *always* left-justified.

## 8. (DP section — not applicable)

Not DP (the greedy is forced by the spec). The reusable skill is the **pack-by-indices / render-by-divmod** pipeline — separating "what goes together" from "how it's formatted", the template for any fixed-width layout task.

## 9. Interviewer follow-up

- *"Minimize raggedness instead of packing greedily"* — the real typesetting problem (TeX): cost = sum of squared leftover spaces per line, minimized by DP over "last line starts at i" or the SMAWK/divide-conquer speedup — a genuine DP extension worth naming.
- *"Center-justify?"* — a fourth render policy: `divmod` the padding into left and right halves. The pipeline absorbs it as one more branch; the packing loop is untouched — which is the payoff of the separation.
- *"Streaming words, emit lines as you go"* — packing is already online (it only ever holds one line's words); only the *last line* policy needs an end-of-stream signal — a nice discussion of why "last" is the one non-local rule in the spec.
- *"Words longer than maxWidth"* — the constraints forbid it; lifting that means hyphenation/breaking policy, i.e. the token definition itself changes. Recognizing which constraint was protecting you is the mark of careful spec reading.
