# Simplify Path — Editorial

## 1. Pattern recognition

Two signals. First, the input has natural delimiters (`/`), which says *tokenize before you think* — never reason about slashes and dots at the character level when `split('/')` hands you clean components. Second, one token (`..`) **cancels the most recent surviving token** — and "cancel the latest thing" is the defining use case for a **stack**. Path canonicalization is the gentlest member of the same family as Decode String and calculator problems: token stream in, stack discipline out.

The interview habit to practice: read the spec out loud and enumerate the token classes. Here that enumeration is *exhaustive* — empty, `.`, `..`, name — and once you've said it, the algorithm is four bullet points.

## 2. Brute force first

The tempting shortcut is string rewriting: repeatedly replace `"//"` with `"/"`, `"/./"` with `"/"`, and regex away `name/..` pairs until nothing changes. Each pass is O(n) and you may need O(n) passes (`/a/b/c/../../..`), so O(n²) — worse, the rewrite rules interact (`/...` must NOT match a `..` rule, `/../` at the root needs its own case) and every fixed rule set tends to leave a corner wrong. The lesson of this problem is precisely that **local text surgery is fragile; tokenize + state machine is robust**.

## 3. The key insight

**Split on `/` and fold the components through a stack — push real names, pop on `..`, ignore `.` and empties — so the stack at the end *is* the canonical path.**

## 4. Step-by-step derivation

1. `path.split('/')` turns all slash-handling into data: a run of `k` slashes yields `k−1` empty strings, and leading/trailing slashes yield empties at the ends. Ignoring empty components implements "collapse repeated slashes" with zero logic.
2. Classify each component: `""` and `"."` → skip; `".."` → pop if the stack is non-empty (popping an empty stack would climb above root — the spec says stay put); anything else → push. Note the order of the checks: `"..."` and `".hidden"` must fall through to the *name* branch, so match `".."` by full equality, never by "starts with dots".
3. The stack now lists the directories from root outward with every cancellation already applied — no second pass needed.
4. Emit `"/" + "/".join(stack)`. This one expression produces `"/"` for an empty stack and never emits a trailing slash — the two formatting bugs this problem is famous for, both solved structurally rather than with `if`s.

## 5. Annotated Python solution

```python
class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in path.split("/"):
            if part == "" or part == ".":
                continue                 # empty (from // or edges) and "here" are no-ops
            if part == "..":
                if stack:                # ".." at root stays at root
                    stack.pop()
            else:
                stack.append(part)       # real name, including things like "..." or ".hidden"
        return "/" + "/".join(stack)
```

## 6. Complexity

- **Time O(n)** — "split visits each character once, and each component is pushed and popped at most once."
- **Space O(n)** — "the component list and the stack are both bounded by the input length."

## 7. Edge-case traps

- **`".."` at the root** (`"/../"`, `"/a/.././.."`) → must silently stay at `/`, not raise or go negative.
- **`"..."` and other all-dot names** — legal directory names; any prefix-based dot matching breaks here.
- **Root output formatting** — result for `"/"`/`"/////"` is exactly `"/"`, not `""` or `"//"`.
- **Trailing slash** (`"/home/"`) must not survive.
- **Names containing dots or underscores** (`"a..b"`, `"_1"`, `".hidden"`) pass through untouched.
- Slash runs interleaved with `.` and `..` (`"/a//b////c/d//././/.."`) — the composed no-ops are where hand-rolled scanners lose track.

## 8. (DP section — not applicable)

Not DP. This trains the **tokenize + stack fold** template — the same delimiter-split-then-stack discipline that scales up to Decode String and the calculator family.

## 9. Interviewer follow-up

- *"Support relative paths"* — input may not start with `/`: keep the stack, but now `..` on an empty stack must be *preserved* (emit leading `../` components) instead of dropped; the classification table grows one row, the structure stays.
- *"Support `~` or environment variables"* — expansion becomes a pre-tokenization pass; the fold is unchanged. This is the practical argument for separating lexing from evaluation.
- *"Symlinks?"* — canonicalization now depends on the filesystem (a `..` after a symlink is not a pure string operation) — a good systems-awareness answer is to name `realpath` semantics and note that pure string simplification is only correct in a symlink-free world.
