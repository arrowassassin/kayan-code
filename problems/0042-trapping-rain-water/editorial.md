# Trapping Rain Water — Editorial

## 1. Pattern recognition

The global-sounding question ("how much water in total?") decomposes into a **per-position** question: how high is the water surface directly above cell `i`? Whenever a per-cell answer depends only on an aggregate of everything to the left and everything to the right, you should smell **prefix/suffix maxima** — and whenever both aggregates are *running maxima*, there's usually a two-pointer refinement that drops the arrays. This is the terrain-following extension of Container With Most Water: same two walls, but now the floor between them matters.

## 2. Brute force first

For each position, scan left for the tallest wall, scan right for the tallest wall, add `min(left, right) - height[i]` if positive: O(n²) time. At `n ≈ 10^5` that is ~10¹⁰ comparisons — a deep valley input makes this hopeless within 3 seconds. But notice the brute force is *conceptually correct*; everything after this is pure precomputation.

## 3. The key insight

**The water level above cell `i` is exactly `min(max(height[0..i]), max(height[i..n-1]))` — and while walking inward from both ends, the smaller of the two running maxima is already final, so that side's cell can be settled immediately.**

## 4. Step-by-step derivation

**Version 1 — prefix-max arrays, O(n) time / O(n) space.** Precompute `left[i] = max(height[0..i])` in one forward pass and `right[i] = max(height[i..n-1])` in one backward pass. Then `water_i = min(left[i], right[i]) - height[i]` (never negative, since both maxima include `height[i]` itself — a tidy way to avoid `max(0, ...)`). Three clean passes; say this version first in an interview, it's fully correct and takes two minutes.

**Version 2 — two pointers, O(n) time / O(1) space.** The only thing `min(left[i], right[i])` needs is the *smaller* side — the larger one is irrelevant beyond knowing it's larger. Walk `lo` and `hi` inward, maintaining `max_left` (max over the consumed left prefix) and `max_right` (consumed right suffix). When `max_left <= max_right`: the true full-array right-max for cell `lo+1` is *at least* `max_right >= max_left`, so `min(true_left, true_right) = max_left'` exactly — the unknown remainder of the right side can only raise a maximum we've already established doesn't bind. That is the answer to the interviewer's "why may you settle that cell without seeing the rest of the array?": the pending side is bounded below by a value that already exceeds the binding side. Advance `lo`, fold the new height into `max_left`, add `max_left - height[lo]`. Mirror when `max_right < max_left`. Each step retires one cell with its final water amount; no cell is ever revisited.

The invariant, stated once: *every cell outside `(lo, hi)` has been credited its exact water, and `max_left`/`max_right` are the true maxima of the consumed ends.*

## 5. Annotated Python solution

```python
class Solution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0
        lo, hi = 0, len(height) - 1
        max_left, max_right = height[lo], height[hi]
        water = 0
        while lo < hi:
            if max_left <= max_right:
                lo += 1                          # left side binds: its level is final
                max_left = max(max_left, height[lo])
                water += max_left - height[lo]   # >= 0 since max_left includes height[lo]
            else:
                hi -= 1
                max_right = max(max_right, height[hi])
                water += max_right - height[hi]
        return water
```

The array version, for reference:

```python
class Solution:
    def trap(self, height: list[int]) -> int:
        n = len(height)
        if n == 0:
            return 0
        left, right = [0] * n, [0] * n
        left[0], right[n - 1] = height[0], height[n - 1]
        for i in range(1, n):
            left[i] = max(left[i - 1], height[i])
        for i in range(n - 2, -1, -1):
            right[i] = max(right[i + 1], height[i])
        return sum(min(left[i], right[i]) - height[i] for i in range(n))
```

## 6. Complexity

- **Two-pointer: time O(n), space O(1)** — "each step permanently settles one cell; state is two maxima and two indices."
- **Prefix arrays: time O(n), space O(n)** — "three linear passes; the arrays trade memory for a simpler proof."

## 7. Edge-case traps

- **Monotone profiles** (`[1,2,3,4,5]` or reversed) — all water drains; answer 0, and the binding-side updates must not go negative.
- **Empty array / single column / two columns** — nothing can be enclosed; guard or let the loop fall through.
- **Update the max *before* adding water** — folding `height[i]` into the running max first is what keeps `max - height[i] >= 0`; swapping those two lines is the classic off-by-one here.
- **Plateaus and equal walls** (`[3,0,3]`, ties between `max_left` and `max_right`) — the `<=` tie-break must still make progress every iteration.
- **Deep V-shaped valley at scale** — the stress case; an O(n²) per-cell scan dies, both O(n) versions cruise.

## 8. Reusable template

Not DP. The trainable skill is the **"per-position answer = min of prefix aggregate and suffix aggregate"** template, plus the two-pointer refinement that keeps only the binding side — the same pairing shows up in Product of Array Except Self (arrays form) and Container With Most Water (pointer form).

## 9. Interviewer follow-up

- *"2-D version: water trapped on a heightmap"* — Trapping Rain Water II (407): the min-of-two-sides argument becomes "water enters from the lowest point of the boundary", solved with a min-heap flood from the border; be ready to explain why per-row 1-D passes are wrong.
- *"The heights arrive as a stream, left to right"* — you can maintain `left` online but not `right`; discuss buffering until a new global max arrives (everything before a running max can be settled) — a nice systems-flavored tangent.
- *"Monotonic stack version?"* — a third O(n) approach that fills basins layer by horizontal layer when a right wall pops lower bars; worth naming to show breadth even if you code the pointer version.
