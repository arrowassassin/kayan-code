# Generate Parentheses — Editorial

## 1. Pattern recognition

"Return **all** well-formed strings" with `n <= 8` — the enumerate-everything signature with a bound so small it's practically a wink. The output count is the Catalan number `C(n)` (1,430 at n = 8), which grows like `4^n / n^1.5`: exponential output means exponential work is *intended*, and the tool for "generate all X satisfying a validity rule" is backtracking. The special flavor here: the validity rule is over *prefixes*, which is exactly the situation where backtracking beats generate-and-filter — you can refuse to extend an invalid prefix the instant it would go wrong, instead of discovering the damage at the end.

## 2. Brute force first

Enumerate all `2^(2n)` bracket strings (each position independently `(` or `)`), then keep the balanced ones — a stack scan or counter check per string. That's `O(2^(2n) · n)`: 65,536 candidates at n = 8, of which barely 2% are valid. It passes at these bounds, and saying so is fine — but the interviewer picked this problem to see whether you'll *construct* validity instead of *checking* it. The gap between `2^(2n)` and `C(n)` is pure wasted work, and closing it requires one observation about prefixes.

## 3. The key insight

**A partial string can be extended to a valid one if and only if `opened < n` permits another `(` and `closed < opened` permits another `)` — enforce those two rules at every step and invalid strings are never built at all.**

## 4. Step-by-step derivation

1. Characterize well-formed strings by their prefixes: a string is balanced iff every prefix has `#( >= #)` and the total counts are equal. This turns a whole-string property into a *local, incremental* one — the pivot of the entire solution.
2. So build left to right carrying two counters. Placing `(` is legal whenever `opened < n` — we can't overspend our budget of n opens, but an extra open never invalidates a prefix. Placing `)` is legal only when `closed < opened` — otherwise this `)` has nothing to match and the prefix is dead beyond repair.
3. These rules are not merely necessary; they're **sufficient**: any prefix respecting them can always be completed (close everything that's open, having spent remaining opens first). That's why there is no validation at the bottom — reaching length `2n` *proves* the string is valid. In tree terms: the brute force explores a tree of 2^(2n) leaves and prunes nothing; this tree has exactly `C(n)` leaves and every leaf is an answer.
4. The recursion is the standard template with two branches instead of a loop: try `(` — append, recurse, pop; try `)` — append, recurse, pop. The pops matter for the usual reason: `path` is shared, and the `)` branch must see the string exactly as it was before the `(` branch ran.
5. Each valid string is produced by exactly one root-to-leaf path (the characters *are* the choices), so no dedup is ever needed.

## 5. Annotated Python solution

```python
class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res = []
        path = []                          # shared partial string, as a list

        def backtrack(opened: int, closed: int) -> None:
            if len(path) == 2 * n:
                res.append("".join(path))  # rules guarantee validity: no check needed
                return
            if opened < n:                 # budget left -> '(' is always safe
                path.append("(")
                backtrack(opened + 1, closed)
                path.pop()                 # unchoose before trying the other branch
            if closed < opened:            # ')' needs an unmatched '(' to close
                path.append(")")
                backtrack(opened, closed + 1)
                path.pop()

        backtrack(0, 0)
        return res
```

## 6. Complexity

- **Time O(C(n) · n)**, where `C(n) ~ 4^n / n^1.5` is the n-th Catalan number — "the tree has one leaf per valid string and no dead branches; each answer costs O(n) to join."
- **Space O(n)** beyond the output — "recursion depth and the shared path are both 2n."

## 7. Edge-case traps

- **`closed < n` instead of `closed < opened`** — the classic wrong guard: it generates garbage like `")("`, because it only budgets `)` counts without requiring a matching `(` first.
- **Missing `path.pop()`** between the two branches — the `)` branch runs on a string still carrying the `(` branch's characters; outputs come out too long and malformed.
- **Appending `path` instead of a joined copy** — aliasing; also, forgetting `"".join` and returning lists of chars.
- **n = 1** — must return exactly `["()"]`; off-by-one in the length check (`2 * n`) shows up here first.
- **Validating at the leaves anyway** — not wrong, but it signals you don't trust (or didn't see) the sufficiency argument in Section 4.

## 8. (DP section — not applicable)

Not DP. This problem trains the choose→explore→unchoose template with **legality guards instead of a candidate loop** — the same "only generate what's still completable" discipline that powers N-Queens' constraint sets and Word Search's pruned grid walk.

## 9. Interviewer follow-up

- *"Multiple bracket types, e.g. `()[]`"* — the counter pair becomes a stack of currently-open bracket kinds; `)` -style choices are legal only when they match the stack top. Same tree, richer guard.
- *"Count the valid strings instead of listing them"* — the answer is Catalan; derive it with the DP `C(k) = sum C(i)·C(k-1-i)` (first matching pair splits the string) — the moment output stops being exponential, DP replaces enumeration.
- *"Generate the k-th string lexicographically without building all of them"* — walk the same tree, but at each node compute how many leaves the `(` subtree contains (Catalan-style counting) and descend left or right accordingly — a nice bridge from enumeration to combinatorics.
- *"Fix a string by removing the fewest brackets"* — Remove Invalid Parentheses (301): BFS/backtracking over deletions, with the same prefix-counter validity test at its core.
