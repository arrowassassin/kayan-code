# Container With Most Water — Editorial

## 1. Pattern recognition

The answer ranges over **pairs of indices**, the score is a simple function of the pair (`min` of heights × distance), and `n = 10^5` rules out quadratic work. That combination — "best pair, too many pairs to try" — is the signature of the **converging two-pointer** technique with a *pruning* argument: start from the widest pair and prove, at every step, that one whole family of pairs can be discarded unseen. Unlike Two Sum II, the input here is *not* sorted; what plays the role of order is the monotone width: it only shrinks as pointers move inward, which is exactly the precondition the exchange argument leans on.

## 2. Brute force first

Try all pairs and keep the max: O(n²) time, O(1) space. At `n = 10^5` that is ~5×10⁹ evaluations — far past a 3-second budget. There is no sorting shortcut either: sorting destroys the positions, and the score depends on distance. We need a way to evaluate only O(n) of the O(n²) pairs while *proving* the skipped ones can't win.

## 3. The key insight

**From any pair, the shorter wall is finished: every remaining container using it is at most as tall and strictly narrower, so discarding the shorter wall discards only provably worse candidates.**

## 4. Step-by-step derivation

1. Start at maximum width: `lo = 0`, `hi = n - 1`. Record its area.
2. Say `height[lo] <= height[hi]`. Consider *every* other container that still uses wall `lo`, i.e. pairs `(lo, j)` with `j < hi`. Its water level is `min(height[lo], height[j]) <= height[lo]` — the cap can't exceed the shorter wall we already have — and its width `j - lo < hi - lo` is strictly smaller. So each such container's area is ≤ the one we just recorded. This is the exchange argument interviewers probe with *"why are you allowed to skip those pairs?"*: we're not guessing that moving the short pointer is good, we're proving the pairs we skip are dominated by a pair already scored.
3. Therefore wall `lo` can never participate in a strictly better container — retire it: `lo += 1`. Symmetric case for `hi` when it's shorter.
4. On a tie either move is safe (both walls are "the shorter one", so both arguments apply); the code moves `lo` for determinism.
5. Invariant view: *the best pair overall is either already recorded or still spans `[lo, hi]`*. Each of the n − 1 steps preserves it, and when the pointers meet, `best` holds the answer.

## 5. Annotated Python solution

```python
class Solution:
    def maxArea(self, height: list[int]) -> int:
        lo, hi = 0, len(height) - 1
        best = 0
        while lo < hi:
            if height[lo] <= height[hi]:
                best = max(best, height[lo] * (hi - lo))
                lo += 1        # all (lo, j<hi) pairs: cap <= height[lo], width smaller
            else:
                best = max(best, height[hi] * (hi - lo))
                hi -= 1        # mirror argument
        return best
```

(Computing `min(...)` explicitly is fine too; branching on the comparison just reuses it as the cap.)

## 6. Complexity

- **Time O(n)** — "one pointer retires per step, so at most n − 1 steps."
- **Space O(1)** — "two indices and a running best."

## 7. Edge-case traps

- **Moving the *taller* pointer** — the classic wrong greedy; `[6,1,1,1,1,1,1,7]` punishes it, since the answer needs both end walls and any premature inward move on the tall side loses.
- **Zero heights** (`[0,0]`) — the answer can legitimately be 0; don't initialize `best` to anything but 0.
- **Equal walls everywhere** (`[5,5,5,5,5]`) — width dominates; the very first pair is optimal, ties must not cause both pointers to move at once past it before recording.
- **Two elements** — the loop must execute exactly once.
- **Best pair strictly interior** (`[1,8,6,2,5,4,8,3,7]` → walls 8 and 7) — confirms the scan doesn't just score the endpoints.

## 8. Reusable template

Not DP. This trains the **two-pointer with a dominance/exchange argument** template — same reasoning style powers Trapping Rain Water (this problem's follow-up), where the shorter side again decides which pointer is safe to advance.

## 9. Interviewer follow-up

- *"Now the ground between walls has terrain and water fills every valley"* — that is Trapping Rain Water (42), the linked extension: the per-cell water level is `min(max-to-left, max-to-right)`, and the same shorter-side pointer logic resolves it in O(n)/O(1).
- *"Return the pair of indices, not just the area"* — track argmax alongside `best`; the proof is unchanged.
- *"Why not divide and conquer or DP?"* — worth answering: the score isn't decomposable over subranges (the best pair may straddle any split), while the dominance argument gives linear time directly; a DP table over pairs is just the brute force in disguise.
