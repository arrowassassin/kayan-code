# Combination Sum — Editorial

## 1. Pattern recognition

"Return **every** unique combination", values ≤ 40, target ≤ 40 — again the *enumerate-all* signature with tiny bounds, so this is backtracking by design. What makes it a step up from Subsets (this problem's linked warmup) is that not every node of the decision tree is an answer anymore: a partial path is only recorded when a **condition** (sum equals target) is met, and — the real teaching point — partial paths can be **proven hopeless early** and cut off. Recognizing "unbounded reuse + unordered combinations" should also trigger a disambiguation reflex in the interview: if the problem asked for the *count* it would be Coin Change-style DP; because it asks for the combinations themselves, the output can be exponential and backtracking is the intended tool.

## 2. Brute force first

The naive tree tries every candidate at every level until the sum reaches or overshoots the target — with no ordering rule, it generates `[2,2,3]`, `[2,3,2]` and `[3,2,2]` separately and needs a sorted-tuple set to deduplicate. That's both wasteful (the same multiset is rebuilt once per permutation — up to `k!` times for a length-`k` combination) and ugly. Worse, without pruning, a branch whose sum already exceeds the target may still spawn children before each one individually fails. The fix for both is structural, not a data structure bolted on afterwards.

## 3. The key insight

**Force each combination into a canonical order by never choosing a candidate with a smaller index than the last choice — passing `start = i` (not `i + 1`) allows reuse while still generating every multiset exactly once.**

## 4. Step-by-step derivation

1. Start from the Subsets skeleton: `backtrack(start)` loops `i` from `start`, choose → explore → unchoose. In Subsets, recursing with `i + 1` meant "each element at most once". Here, recursing with `i` means "you may pick `candidates[i]` again, but never anything *before* it". Every multiset then appears exactly once — as its index-sorted spelling — and deduplication disappears by construction.
2. Add the goal condition: carry `remaining` (target minus the path sum) as a parameter; when `remaining == 0`, record `path[:]` and return. Decrementing a parameter beats re-summing the path — O(1) per node instead of O(k).
3. **Prune.** A candidate larger than `remaining` cannot help, and since candidates are all positive, nothing downstream of it in that branch can recover. Skipping it is a per-item prune; the stronger move is:
4. **Sort first, then `break`.** With `candidates` sorted ascending, the first candidate that exceeds `remaining` proves every later candidate does too — so `break` abandons the entire rest of the level, not just one item. On a case like `candidates=[2,3,5,7,11,13], target=30`, the deep-left branches full of 2s die the instant `remaining` drops below 2, instead of testing all six candidates at every dead node. Sorting costs O(k log k) once and pays for itself immediately.
5. Termination is guaranteed because every candidate is ≥ 2 (> 0 is enough): `remaining` strictly decreases, so depth is at most `target / min(candidates)`.

## 5. Annotated Python solution

```python
class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()                 # ascending -> the break-prune below is valid
        res = []
        path = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                res.append(path[:])       # copy: path keeps mutating after this
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break                 # sorted: every later candidate is too big too
                path.append(candidates[i])               # choose
                backtrack(i, remaining - candidates[i])  # i, NOT i+1: reuse allowed
                path.pop()                               # unchoose

        backtrack(0, target)
        return res
```

## 6. Complexity

- **Time O(k^(T/m))** in the worst case, where `k` = number of candidates, `T` = target, `m` = smallest candidate — "the tree has branching factor up to k and depth up to target over the smallest candidate; it's exponential, which is why target is capped at 40." The sort-prune doesn't change the bound but slashes the constant by killing dead branches at first contact.
- **Space O(T/m)** beyond the output — "the recursion stack and path are at most as deep as the longest combination."

## 7. Edge-case traps

- **`i + 1` instead of `i`** — quietly forbids reuse; `[2], target 4` returns `[]` instead of `[[2,2]]`.
- **`start` dropped entirely** (looping from 0 every level) — generates every permutation of every combination; the dedup set that "fixes" it is the bug's confession.
- **Missing `path.pop()`** — the unchoose half of the template; siblings inherit choices they never made.
- **No solution exists** (`[2], target 1`; `[4,6], target 11` — parity makes 11 unreachable) — must return `[]`, and the pruned tree should die fast.
- **Target equal to a single candidate** — the length-1 combination `[7]` is easy to lose if the `remaining == 0` check sits in the wrong place.
- **Pruning with `continue` instead of `break`** after sorting — still correct but forfeits the point of sorting; interviewers notice.

## 8. (DP section — not applicable)

Not DP (the *count* version would be). This problem trains the choose→explore→unchoose template **plus** the two upgrades that carry to all harder backtracking: canonical ordering via the `start` index, and sort-enabled pruning.

## 9. Interviewer follow-up

- *"Each candidate usable at most once, input may contain duplicates"* — Combination Sum II (40): recurse with `i + 1`, and after sorting skip `i > start and candidates[i] == candidates[i-1]` so equal values open only one branch per level.
- *"Exactly k numbers from 1–9"* — Combination Sum III (216): same template, two goal conditions (`remaining == 0` and `len(path) == k`).
- *"Just count the combinations"* — now the output is one number, the exponential excuse vanishes, and it becomes coin-change DP over `target` — worth saying unprompted.
- *"What if candidates could be negative?"* — termination breaks (`remaining` no longer decreases monotonically); you'd need a depth cap or a bound on combination length to make the problem well-posed.
