# Decode String — Editorial

## 1. Pattern recognition

The grammar is recursive — a `k[chunk]` block can contain further blocks — and recursive grammars are handled one of two equivalent ways: recursive-descent parsing, or a single pass with an **explicit stack** that suspends the outer context while the inner block completes. Balanced brackets plus "finish the innermost thing first" is the stack signature, the same one behind Valid Parentheses and Basic Calculator. Before coding, enumerate the token classes out loud: digits (accumulate a number), `[` (enter a block), `]` (leave a block), letters (append). Four classes, four branches — the loop writes itself once the classes are named.

## 2. Brute force first

Textual expansion: repeatedly find an *innermost* `k[chunk]` (one with no brackets inside), replace it with `chunk * k`, repeat until no brackets remain. Each rewrite rescans and rebuilds the string, and with nesting the intermediate strings grow before shrinking: O(passes × output length), comfortably quadratic-plus. On `9[9[9[9[9[ab]]]]]` (output ~118k chars) it still finishes, but the deeper flaw is architectural: rewriting text you'll re-parse next pass is exactly what the parse-don't-rewrite discipline exists to avoid. Parse once; never re-read your own output.

## 3. The key insight

**On `[`, push the partially built outer string and the pending count, then start empty; on `]`, pop and splice: `current = outer + current * k`.**

## 4. Step-by-step derivation

1. Scan left to right holding two registers: `cur` (the string being assembled at the current depth) and `num` (the count being read). Digits combine as `num = num * 10 + digit` — the multi-digit trap (`12[`, `100[`) is dodged structurally, never by assuming counts are single characters.
2. `[` means "the block belonging to `num` starts here, and everything I've built so far belongs to my *parent*". So push the pair `(cur, num)` and reset both. The stack frame is exactly the suspended parent context — this is hand-rolled recursion.
3. `]` means the innermost block just finished: pop `(outer, k)` and splice with `outer + cur * k`. Innermost-first ordering is guaranteed because the nearest unmatched `[` is always on top of the stack.
4. Letters simply extend `cur`.
5. One Python performance point: keep `cur` as a **list of pieces** and join late. `str + str` in a loop copies the accumulated prefix every time; with 10⁵-character outputs that's the difference between linear and quadratic.

## 5. Annotated Python solution

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []       # frames of (outer_pieces, repeat_count)
        cur = []         # pieces of the string being built at this depth
        num = 0          # multiplier being accumulated digit by digit
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)     # multi-digit counts like 12[
            elif ch == "[":
                stack.append((cur, num))     # suspend the outer context
                cur, num = [], 0
            elif ch == "]":
                outer, k = stack.pop()       # finish this block, resume outer
                outer.append("".join(cur) * k)
                cur = outer
            else:
                cur.append(ch)
        return "".join(cur)
```

## 6. Complexity

- **Time O(n + output)** — "each input character is handled once, and each output character is written a constant number of times thanks to late joining."
- **Space O(output)** — "the stack depth is bounded by the nesting, and the buffers together hold at most the decoded result."

## 7. Edge-case traps

- **Multi-digit counts** (`10[a]`, `100[x]`) — the number register must accumulate, not overwrite.
- **No brackets at all** (`"abc"`) — the loop must degrade to a plain copy; final answer comes from `cur`, not from a pop.
- **Text after the last `]`** (`2[b3[a]]x`) — trailing letters land in the restored outer buffer; solutions that return on `]` miss them.
- **Deep nesting** (`2[2[2[2[ab]]]]`) — exercises the suspend/resume order; the classic bug is pushing `num` *after* resetting it.
- **Adjacent sibling blocks** (`3[a]2[bc]`) — state must fully reset between blocks.

## 8. (DP section — not applicable)

Not DP. This trains the **stack-of-suspended-contexts** template — hand-rolled recursive descent — which reappears verbatim in Basic Calculator's parenthesized expressions and in nested-structure parsers generally.

## 9. Interviewer follow-up

- *"Now evaluate arithmetic instead of repeating text"* — that is Basic Calculator II (227), this problem's linked extension: same single-pass token loop, but the stack holds signed terms and precedence replaces nesting.
- *"Input may be malformed"* — turn the guarantees into checks: `]` with an empty stack, `[` without a preceding count, digits before end-of-string, leftover frames at the end. Enumerating failure tokens is the same skill as enumerating token classes.
- *"Decoded output is gigabytes"* — don't materialize it: keep the parse tree (`k × children`) and expose length queries / k-th character lookups by walking the tree — a common follow-up (LC 880 is this exact idea).
- *"Write it recursively"* — a `parse(i)` returning `(decoded, next_index)`; the explicit stack and the call stack are interchangeable, and saying so is the point.
