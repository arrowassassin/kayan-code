# Reverse Words in a String — Editorial

## 1. Pattern recognition

The statement bundles three normalizations — reverse word order, squash internal space runs, trim the edges — and messy-whitespace strings are the tell for the **tokenize, then reassemble** pattern. The moment you separate *lexing* (find the words) from *output formatting* (join them), all three requirements become one line of logic. Trying to do it as in-place character surgery on the original string is how candidates drown in special cases.

## 2. Brute force first

There's no complexity cliff here — every reasonable approach is O(n). The "brute force" axis is instead *how much machinery you deploy*: building the character-by-character output with flags for "was the last char a space?" is the fragile version, easy to get subtly wrong at the boundaries. The measure of quality is edge-case robustness, not big-O. In Python the pragmatic answer is `" ".join(reversed(s.split()))` — genuinely correct, because argument-less `split()` is *defined* to drop leading/trailing whitespace and treat runs as one separator. Say that sentence to the interviewer; it proves you know the library's contract rather than being lucky.

## 3. The key insight

**Lex first, format second: extract maximal non-space runs as tokens, and the reversal, collapsing, and trimming all become properties of the join, not of the scan.**

## 4. Step-by-step derivation

1. Define the token: a maximal run of non-space characters. That definition already implies space runs contribute nothing and edge spaces contribute nothing — enumerate the token classes (word chars, spaces) and the spec is half-implemented.
2. To show parsing skill rather than library recall, scan **from the right** so tokens come out already in output order — no `reversed` needed.
3. Each iteration does two walks: skip spaces (may hit the string start — that's the clean exit), then walk left through the word. The word is `s[j+1 : i+1]`: `j` stopped *on* the space (or at −1), `i` sits on the word's last char. Both `+1`s exist because the walks overshoot by one — say that out loud; it's the off-by-one audit.
4. Join with a single space. Emitting separators during the scan instead of joining at the end is what creates trailing-space bugs.
5. For the classic O(1)-extra-space variant (on a mutable char array): reverse the whole array, then reverse each word in place, then compact spaces with a read/write pointer — same tokenization idea, expressed as swaps.

## 5. Annotated Python solution

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        words = []
        i = len(s) - 1
        while i >= 0:
            # skip any run of spaces
            while i >= 0 and s[i] == " ":
                i -= 1
            if i < 0:
                break
            # scan the word we just landed on
            j = i
            while j >= 0 and s[j] != " ":
                j -= 1
            words.append(s[j + 1:i + 1])
            i = j
        return " ".join(words)
```

## 6. Complexity

- **Time O(n)** — "each character is visited by exactly one of the two inner walks, once."
- **Space O(n)** for the output — "the token list is the answer; in-place O(1) is only meaningful on a mutable char array."

## 7. Edge-case traps

- **Leading/trailing spaces** (`"  hello world  "`) — the final join must not reproduce them.
- **Multi-space runs between words** — collapse to one; scan-and-emit solutions typically leak a double space here.
- **Single word**, with or without padding → the word itself, no spaces.
- **One-character words** (`"a b"`) — stresses the `j+1 : i+1` slice arithmetic.
- **Punctuation and digits are word characters** (`"x2, y7!"`) — only `' '` separates; don't reach for `isalpha`.

## 8. (DP section — not applicable)

Not DP. This trains the **right-to-left tokenizer** template — skip-delimiters / consume-token loops with an overshoot-then-`+1` slice — the same skeleton used in Simplify Path and Compare Version Numbers.

## 9. Interviewer follow-up

- *"Do it in place with O(1) extra space"* — assume a mutable `list[str]`: reverse everything, reverse each word, then two-pointer compact the spaces. Walk through why reversal-of-reversals restores letter order.
- *"Multiple delimiter characters (tabs, commas)?"* — only the skip predicate changes; the tokenize-then-join structure is untouched. That separation is the point of the pattern.
- *"What if the string doesn't fit in memory?"* — read blocks from the end of the file backwards, carrying a partial-word buffer across block boundaries; the right-to-left scan generalizes directly.
