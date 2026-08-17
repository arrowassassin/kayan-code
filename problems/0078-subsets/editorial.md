# Subsets — Editorial

## 1. Pattern recognition

Two words in the statement give the game away: "**every** possible subset" and `len(nums) <= 10`. When a problem asks for *all* configurations (not the best one, not the count) and the input bound is tiny — 10, 15, 20 — the intended solution is **exhaustive enumeration via backtracking**. The bound is not the author being lazy: the answer itself has `2^n` entries, so *no* algorithm can beat exponential, and `n <= 10` (1,024 subsets) is the author telling you that's fine. Subsets is the cleanest possible specimen of the choose→explore→unchoose template, which is why it's the warmup for the whole Backtracking family.

## 2. Brute force first

There is no "brute force vs. optimal" gap here in the usual sense — output size forces Θ(2^n) on everyone. The naive approaches that *do* go wrong are structural, not asymptotic: generating subsets by looping over all sizes and hand-rolling nested loops (breaks the moment `n` isn't fixed), or generating candidate lists with duplicates and deduplicating through a set of tuples (works, but tells the interviewer you couldn't enumerate cleanly). The interview task is to produce each subset **exactly once, by construction**.

## 3. The key insight

**Every subset is the outcome of n independent yes/no decisions — walk the binary decision tree, and each node's partial path is itself a valid subset.**

## 4. Step-by-step derivation

1. Fix an order on the elements. A subset is then fully described by which indices it takes — so build it left to right, deciding one index at a time.
2. Recursion state: `path` (elements chosen so far) and `start` (first index not yet decided). Passing `start` forward means we only ever *add* indices larger than any already taken — that's what guarantees each subset is generated exactly once, with no dedup pass.
3. At each call, first **record** `path[:]`. Recording at every node (rather than only at "leaves") works because a partial choice like `[1]` is a complete, legitimate subset — there is no validity condition to wait for.
4. Then loop `i` from `start`: `path.append(nums[i])` (choose), `backtrack(i + 1)` (explore), `path.pop()` (unchoose). The pop restores `path` to exactly what it was before the iteration, so the next `i` starts from a clean slate. This mutate-recurse-undo discipline is the template every harder backtracking problem (Combination Sum, N-Queens, Word Search) reuses verbatim.
5. Copy on record (`path[:]`, not `path`) — `path` is one shared, mutated list; appending the reference would make every "subset" in the result alias the same (eventually empty) list.

**The iterative doubling alternative.** Start from `res = [[]]`. For each number `x`, set `res += [s + [x] for s in res]` — every existing subset spawns a twin that includes `x`, doubling the count. After all `n` numbers, `res` holds all `2^n` subsets. It's the same binary decision, expressed breadth-first instead of depth-first, and it's a great answer to "can you do it without recursion?" (So is counting from `0` to `2^n - 1` and reading each bitmask as an in/out vector.)

## 5. Annotated Python solution

```python
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        path = []                         # the one shared partial subset

        def backtrack(start: int) -> None:
            res.append(path[:])           # record a COPY: every node is a valid subset
            for i in range(start, len(nums)):
                path.append(nums[i])      # choose
                backtrack(i + 1)          # explore: only indices after i -> no duplicates
                path.pop()                # unchoose: restore state for the next branch

        backtrack(0)
        return res
```

## 6. Complexity

- **Time O(n · 2^n)** — "there are 2^n subsets and copying each one costs up to n; you cannot do better because that's the size of the output."
- **Space O(n)** beyond the output — "the recursion stack and the shared path are both at most n deep."

## 7. Edge-case traps

- **Appending `path` instead of `path[:]`** — the classic aliasing bug: the result ends up as 2^n references to one empty list.
- **Forgetting `path.pop()`** — sibling branches inherit elements they never chose; the output has wrong, oversized subsets. This is the "unchoose" half of the template and the thing hidden tests punish.
- **Recursing with `start` instead of `i + 1`** — re-picks the same element and never terminates (or duplicates wildly).
- **Missing the empty subset** — recording only at leaves, or seeding the iterative version with `[]` instead of `[[]]`.
- **Single-element input** — must yield exactly `[[], [x]]`.

## 8. (DP section — not applicable)

Not DP. This problem trains the reusable **choose→explore→unchoose** backtracking template in its purest form — the same skeleton, plus a pruning condition, becomes Combination Sum (this problem's linked follow-up), and plus constraint sets becomes N-Queens.

## 9. Interviewer follow-up

- *"What if `nums` contains duplicates?"* — Subsets II (90): sort first, then inside the loop skip `i > start and nums[i] == nums[i-1]`, so each duplicate value only starts a branch once per level.
- *"Only subsets of size k"* — Combinations (77): record `path` only when `len(path) == k`, and prune when fewer than `k - len(path)` elements remain.
- *"Subsets summing to a target, elements reusable"* — that is Combination Sum (39), the linked extension: same tree, but a running-sum bound decides both recording and pruning.
- *"No recursion allowed"* — give the doubling loop or the bitmask enumeration from Section 4.
