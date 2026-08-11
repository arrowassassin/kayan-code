# Sort Colors — Editorial

## 1. Pattern recognition

"Sort" plus "only three distinct values" plus "in place, one pass" — the value set is so small that the ordering problem collapses into a **partitioning** problem. This is the classic **Dutch national flag** (Dijkstra): maintain growing sorted zones at both ends and an unknown zone that shrinks to nothing. It's the three-way sibling of the two-way partition inside quicksort. Interviewers love it because the algorithm is five lines and every line has a trap.

## 2. Brute force first

Any library or comparison sort is O(n log n) and explicitly banned. The honest baseline is **counting sort**: one pass to count 0s/1s/2s, one pass to rewrite — O(n) time, O(1) space, completely correct. Say it, then note its two drawbacks for the interview: it's two passes over the data, and it *rewrites* rather than *moves* elements, which stops working the moment elements are records with a color key rather than bare integers. That's the cue for the one-pass swap-based version.

## 3. The key insight

**Keep the array split into four zones — known 0s, known 1s, unknown, known 2s — and each step classifies one unknown element by swap, shrinking the unknown zone by exactly one.**

## 4. Step-by-step derivation

1. Pointers: `lo` = first slot that's not a confirmed 0; `mid` = first unexamined slot; `hi` = last unexamined slot. Invariant: `nums[:lo]` are all 0, `nums[lo:mid]` all 1, `nums[hi+1:]` all 2, `nums[mid:hi+1]` unexamined. Initially `lo = mid = 0`, `hi = n - 1`: the whole array is unknown, all sorted zones empty — the invariant holds vacuously.
2. Examine `nums[mid]`. If **1**: it's already where 1s live; `mid += 1`.
3. If **0**: swap `nums[lo] <-> nums[mid]`, advance both. Why is advancing `mid` safe? Because the element that arrived came from `nums[lo]`, which sits inside the known-1 zone (or equals `mid` itself when that zone is empty) — either way it's a value we've already classified, so there is nothing left to examine.
4. If **2**: swap `nums[mid] <-> nums[hi]`, `hi -= 1`, and **leave `mid` alone**. The element that arrived came from the *unknown* zone — we have never looked at it, and advancing past it is the bug that breaks inputs like `[2,0,1]`. This asymmetry (0-swap advances mid, 2-swap doesn't) is the whole exam.
5. Loop **while `mid <= hi`** — inclusive, because `nums[hi]` itself is still unexamined; `mid < hi` leaves one element unclassified. Termination: every branch either advances `mid` or retreats `hi`, so the unknown zone strictly shrinks. When it empties, the three zones tile the array — sorted.

## 5. Annotated Python solution

```python
class Solution:
    def sortColors(self, nums: list[int]) -> None:
        lo, mid, hi = 0, 0, len(nums) - 1
        # invariant: [0..lo) zeros | [lo..mid) ones | [mid..hi] unknown | (hi..n) twos
        while mid <= hi:                       # <=: nums[hi] is still unexamined
            if nums[mid] == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1
                mid += 1                       # incoming value was already classified
            elif nums[mid] == 1:
                mid += 1
            else:  # nums[mid] == 2
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1                        # incoming value is UNexamined: keep mid
```

## 6. Complexity

- **Time O(n)** — "every iteration shrinks the unknown zone by one, and swaps are O(1)."
- **Space O(1)** — "three indices; the array is rearranged in place."

## 7. Edge-case traps

- **Advancing `mid` after a 2-swap** — the signature bug; `[2,0,1]` or a leading run of 2s exposes it immediately.
- **`mid < hi` instead of `mid <= hi`** — leaves the last unknown element unclassified; `[1,2,0]` catches it.
- **Single-element and all-equal arrays** — the loop body must tolerate zones that never grow (all 1s means no swap ever happens).
- **Already-sorted and reverse-sorted inputs** — reverse-sorted maximizes 2-swaps and stresses the "don't advance mid" rule.
- **Returning a new list** — the judge compares the mutated argument; building a sorted copy and returning it scores WA even if the copy is right.

## 8. Reusable template

Not DP. This trains the **three-way partition** template — the same zone-invariant reasoning powers quicksort's 3-way partition (fat pivot), Move Zeroes (its two-zone little sibling), and any "group by small enum in place" task.

## 9. Interviewer follow-up

- *"k colors instead of 3?"* — one pass no longer suffices with O(1) state per color boundary; options are counting sort (O(n + k), two passes) or repeated two-way partitions; discuss the trade-off.
- *"Prove the invariant"* — be ready to state the four zones and check all three branches preserve them; this problem is a favorite vehicle for "walk me through your loop invariant".
- *"Elements are objects with a color field and swaps are expensive"* — counting sort's rewrite trick dies (you can't fabricate objects); the swap-based flag survives, and you can mention minimizing swaps by skipping already-placed runs.
