# Basic Calculator II — Editorial

## 1. Pattern recognition

An expression grammar with **two precedence levels** and no parentheses. The parsing move is the same single-pass token loop as Decode String (this problem's warmup): enumerate the token classes out loud — digits, the four operators, spaces — and give each a branch. What's new is precedence, and the classic trick for exactly-two-levels is the **stack of resolved terms**: `+`/`-` create new terms, `*`/`/` mutate the most recent one. No operator-precedence tables, no two-stack shunting yard needed.

## 2. Brute force first

Two passes: tokenize, then evaluate all `*`/`/` in a list-rewriting pass, then sum with signs. Correct and still O(n) — but it materializes a token list and rewrites it in place (deletions from the middle can even make it O(n²) if done naively with `list.pop(i)`). The single-pass version does strictly less work and is the version interviewers expect. (`eval` is explicitly off the table — and worth mentioning that in production, a real tokenizer/AST, not regex surgery, is still the answer: expressions are a grammar, and grammars want parsers.)

## 3. The key insight

**Treat the expression as a sum of terms: keep a stack of finished terms, push `±num` on `+`/`-`, and on `*`/`/` fold the incoming number into the stack's top — then the answer is `sum(stack)`.**

## 4. Step-by-step derivation

1. `a - b * c + d` means `a + (-(b*c)) + d`: subtraction is "add a negated term", and `*`/`/` only ever modify the term currently being built. That reframing removes precedence from the control flow entirely.
2. Scan with two registers: `num` (digits accumulate as `num*10 + digit`) and `op`, the operator *waiting to be applied* to `num`. You can't act on a number until you see what follows it — hence the operator lags one token behind.
3. When a new operator arrives, resolve the pending one: `+` → push `num`; `-` → push `-num`; `*` → `stack[-1] *= num` (pop/apply/push); `/` → same with division. Then store the new operator and clear `num`.
4. The **flush trap**: the final number has no operator after it. Fold the resolution into the condition "current char is an operator OR this is the last character" — spaces must *not* trigger resolution, only skip. Getting `" 3 "`-style padding right is exactly why the condition reads `(not digit and not space) or last`.
5. The **division trap**: intermediate terms can be negative even though all literals are non-negative (`0-3/2`: the pending term is `-3`, then `/2`). Python's `//` floors (`-3 // 2 == -2`) but the spec truncates toward zero (`-1`). `int(-3 / 2)` truncates correctly; for full-integer safety with huge operands, `-(-a // b)` when signs differ also works — say which you're using and why.

## 5. Annotated Python solution

```python
class Solution:
    def calculate(self, s: str) -> int:
        stack = []       # resolved terms; '+'/'-' push, '*'/'/' fold into the top
        num = 0
        op = "+"         # operator waiting to be applied to num
        n = len(s)
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)
            # apply the pending op on an operator OR at the very last char
            if (not ch.isdigit() and ch != " ") or i == n - 1:
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    # int(a / b) truncates toward zero; a // b would floor
                    stack.append(int(stack.pop() / num))
                op = ch
                num = 0
        return sum(stack)
```

## 6. Complexity

- **Time O(n)** — "one pass; every character is classified once and each term is pushed and popped at most once."
- **Space O(n)** — "the term stack can hold one entry per `+`/`-`; O(1) if you keep only a running total plus the previous term."

## 7. Edge-case traps

- **Truncation toward zero on negative intermediates** — `"0-3/2"` → `-1`; `//` gives `-2`. The single most common WA.
- **The unflushed last number** — `"42"` or anything not ending in an operator; also the reason the flush check uses `i == n - 1` and not "saw an operator".
- **Spaces anywhere** (`" 3+5 / 2 "`) — must skip without resolving; a space is not an operator.
- **Left-to-right equal precedence** — `"100/3*3"` is `(100/3)*3 = 99`, not `100/(3*3)`; folding into the stack top preserves this order automatically.
- **Multi-digit numbers** (`"1000000/1/2/3"`) — accumulate, don't overwrite.
- **Chained division truncation** — each `/` truncates individually, not once at the end.

## 8. (DP section — not applicable)

Not DP. This trains the **pending-operator scan with a term stack** — the two-precedence-level expression template that extends to Basic Calculator I/III by adding a frame push on `(` (the same suspend/resume move as Decode String).

## 9. Interviewer follow-up

- *"Add parentheses"* — on `(`, push the whole `(stack, op)` context and start fresh; on `)`, collapse the inner sum into a `num` and resume — Basic Calculator III. Your loop body survives intact; only two branches are added.
- *"O(1) space?"* — you never need more than the running sum of *closed* terms plus the current term: replace the stack with `total` and `prev_term`; on `+`/`-` fold `prev_term` into `total`. Walking through that reduction is a strong finish.
- *"Support unary minus"* — a `-` is unary when it follows an operator or start-of-string; it flips a sign attached to the upcoming number. Enumerating *when* a token's meaning depends on its left context is exactly the read-the-spec-aloud habit this family drills.
- *"Exponentiation (right-associative)?"* — precedence climbing / recursive descent; note that the term-stack trick is special to two levels with left associativity.
