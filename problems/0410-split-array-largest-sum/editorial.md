# Split Array Largest Sum — Editorial

## 1. Pattern recognition

"**Minimize the maximum** block sum over all ways to cut the array into `k` contiguous pieces." Two flags fire at once. *Minimize-the-maximum* over partitions is a classic DP shape — and many candidates stop there. But the answer is a single integer, and making the allowed maximum *larger* only ever makes the cutting *easier*: that's the monotonic-feasibility signature from Koko (875) and Ship Packages (1011), this problem's warmup chain. In fact 410 **is** 1011 with the phrasing inverted — "capacity" is the cap on a block sum, "days" is `k`. Recognizing a Hard as a re-costumed Medium is precisely what this chain trains.

## 2. Brute force first

Enumerate cut positions: `C(n-1, k-1)` ways — astronomically many. The honest baseline is interval DP (see section 8): `O(k · n²)` time. At `n = 1000` that's viable; at this problem's `n = 5 · 10^4` it's `2.5 × 10^9` cell-transitions *per layer* — hopeless. The constraints are the tell that the intended solution is not the DP.

## 3. The key insight

**Fix a candidate answer `limit` and the problem inverts into an easy greedy question — "how few contiguous pieces keep every sum ≤ limit?" — and since a bigger limit never needs more pieces, feasibility is monotonic and the answer can be binary searched.**

## 4. Step-by-step derivation

1. **Invert the optimization into a decision.** Hard direction: "given `k` pieces, minimize the max sum." Easy direction: "given a max-sum cap `limit`, minimize the pieces." The easy direction is the Ship Packages greedy verbatim: sweep left to right, extend the current block until the next element would break the cap, then cut. O(n), and optimal by the usual exchange argument — cutting later never forces more pieces.
2. **Feasible means `pieces_needed(limit) <= k`, not `== k`.** If the greedy uses fewer than `k` pieces, split any block again: sums only shrink (elements are non-negative), so a valid exactly-`k` split still exists. This is the subtle point interviewers poke at.
3. **Monotonicity.** Raising `limit` can only let blocks grow, never forces an extra cut, so `pieces_needed` is non-increasing. The answer space reads `F F F T T T`. Say the framing out loud: *"if a cap of `x` works, `x+1` works — so I binary search the answer, not the array."*
4. **Bounds.** `lo = max(nums)` — every element must sit inside some block. `hi = sum(nums)` — one block, `k = 1`. Both are exact answers for degenerate inputs, so the bracket is tight.
5. **Leftmost-true bisect.** `feasible(mid)` → `hi = mid`; else `lo = mid + 1`; the loop invariant "answer ∈ [lo, hi]" holds until `lo == hi`.

## 5. Annotated Python solution

```python
class Solution:
    def splitArray(self, nums: list[int], k: int) -> int:
        def pieces_needed(limit: int) -> int:
            pieces, total = 1, 0
            for x in nums:
                if total + x > limit:     # next element breaks the cap -> cut
                    pieces += 1
                    total = 0
                total += x                # always fits: limit >= max(nums)
            return pieces

        lo, hi = max(nums), sum(nums)     # tight bracket around the answer
        while lo < hi:
            mid = (lo + hi) // 2
            if pieces_needed(mid) <= k:   # <= k, not == k: extra cuts are free
                hi = mid                  # cap achievable -> try smaller
            else:
                lo = mid + 1              # forced past k pieces -> raise cap
        return lo
```

## 6. Complexity

- **Time O(n log S)**, `S = sum(nums)` — "about 35 greedy passes; each candidate cap is verified in one O(n) sweep."
- **Space O(1)** — "two bounds and two counters."

## 7. Edge-case traps

- **`k == 1`** — answer is `sum(nums)`; the search must be able to land on `hi`.
- **`k == len(nums)`** — one element per piece; answer is `max(nums)`, i.e. `lo` returned untouched.
- **Zeros in `nums`** — `limit` can equal 0; the greedy's strict `>` keeps zero-blocks legal, and the `<= k` (pad with free cuts) argument depends on non-negativity — mention it.
- **Contiguity trap** — `[10^6, 1, 10^6, 1, 10^6], k = 3` answers `10^6 + 1`: the big values cannot be pooled or the small ones skipped; blocks are contiguous, so each heavy element anchors its own block plus a neighbor.
- **Sums overflow 32 bits** (`5·10^4 × 10^6 = 5·10^10`) — free in Python; say it for other languages.

## 8. Reusable template — and the DP alternative

Not DP-required, but name the alternative: `dp[i][j]` = best cost splitting the first `i` elements into `j` pieces, `dp[i][j] = min over cut c of max(dp[c][j-1], prefix[i] - prefix[c])` — `O(k·n²)` time, `O(k·n)` space. Binary search wins at scale because it replaces the quadratic "where is the last cut?" enumeration with 
`log(sum)` O(n) feasibility sweeps: `n log S ≈ 1.8 × 10^6` operations versus `2.5 × 10^9`-per-layer for the DP at `n = 5·10^4`. The reusable template is the **binary-search-on-the-answer** frame (monotonic predicate + leftmost-true bisect) shared with 875 and 1011.

## 9. Interviewer follow-up

- *"Recover the actual cut positions"* — rerun the greedy once at the final answer and record where it cuts; O(n) post-pass.
- *"Negative numbers allowed?"* — monotonicity of the greedy predicate breaks (a block's sum can dip and recover), and the pad-to-exactly-`k` argument dies; the DP from section 8 becomes the correct tool. Knowing *when* the template's preconditions fail is worth as much as the template.
- *"Minimize the number of pieces given a cap instead?"* — that's just the predicate, run once.
- *"Streaming / online version?"* — a fixed cap can be checked online in O(1) space, but minimizing needs `max` and `sum` up front; discuss two-pass vs. known-bounds trade-offs.
