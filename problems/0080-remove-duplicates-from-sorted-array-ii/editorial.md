# Remove Duplicates from Sorted Array II — Editorial

## 1. Pattern recognition

"Compress in place, keep relative order, return the new length" is the **reader/writer two-pointer** pattern (also called slow/fast): a read index that visits every element and a write index that marks the end of the accepted prefix, with `write <= read` at all times so writes never clobber unread data. The second signal is **sorted input**: equal values are adjacent, which turns the global condition "at most two copies of each value" into a purely local test — no counting, no hash map. Version I of this problem ("at most once") uses the same skeleton; the interesting part here is discovering how little state "at most twice" actually needs.

## 2. Brute force first

Build a new list, appending each value while a counter for the current run stays ≤ 2, then copy it back: O(n) time but O(n) extra space — and the statement bans it. In-place deletion with `list.pop(i)` on every excess duplicate is O(n) shifting per deletion, O(n²) worst case (30,000 copies of one value ≈ 4.5×10⁸ element moves). The task is to get the O(n)-list-version's simplicity without its memory.

## 3. The key insight

**"Value `x` already has two copies in the kept prefix" is equivalent to one comparison: `nums[write - 2] == x` — because the kept prefix is sorted, its last two slots are the only place a third copy could be sitting.**

## 4. Step-by-step derivation

1. Invariant: `nums[:write]` is exactly the correct compressed output of everything read so far. It's sorted (we only ever append values from a sorted stream) and holds at most two of each value.
2. For the current element `x`, we may append it unless doing so creates a third copy. A third copy requires two `x`s already kept — and since the kept prefix is sorted and `x` is the largest value seen, those two would occupy positions `write - 1` **and** `write - 2`. So the single test `nums[write - 2] == x` (with `write >= 2`) detects it. This is the "why can you skip the count?" answer: sortedness compresses "count of x in the prefix ≥ 2" into one array read.
3. Guard the boundary: when `write < 2` nothing can have two copies yet — always keep. Writing the condition as `write < 2 or nums[write - 2] != x` handles the first two elements without a special-cased loop start, the usual source of off-by-ones here.
4. Compare against `nums[write - 2]`, not `nums[read - 2]`: the *original* array two slots behind the reader may hold a value you already discarded. On `[1,1,1,2]`, reading the `2`, `nums[read - 2]` is a stale `1` — the test would pass for the wrong reason on some inputs and fail on others. The invariant lives at the write side; test it there.
5. Each kept element is written once; each element is read once → O(n), and `write` is the answer `k`.

## 5. Annotated Python solution

```python
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        write = 0
        for x in nums:                          # read pointer
            # keep unless the kept prefix already ends in [x, x]
            if write < 2 or nums[write - 2] != x:
                nums[write] = x                 # safe: write <= read always
                write += 1
        return write
```

## 6. Complexity

- **Time O(n)** — "one pass; each element is read once and written at most once."
- **Space O(1)** — "two indices; the array is compacted in place."

## 7. Edge-case traps

- **Comparing against the original array** (`nums[read - 2]`) instead of the kept prefix — the central bug; long runs followed by a new value expose it.
- **Arrays of length 1 or 2** — must survive untouched; the `write < 2` guard is what makes that automatic.
- **One value repeated many times** — output is exactly two elements; also the case where a pop-based approach quadratically dies.
- **No duplicates at all / everything already at exactly two** — the writer shadows the reader and every element rewrites itself in place; make sure that's harmless.
- **Returning the list instead of `k`** — the judge reads the integer and then inspects `nums[:k]`; both must be right.

## 8. Reusable template

Not DP. The template is the **reader/writer in-place filter**: `for x in nums: if keep(x): nums[write] = x; write += 1`. Swapping the `keep` predicate gives Remove Duplicates I (`nums[write-1] != x`), Remove Element, Move Zeroes, and String Compression.

## 9. Interviewer follow-up

- *"Generalize to at most `k` copies"* — change the test to `nums[write - k] != x`; being able to say why (the last `k` kept slots are the only possible home of `k` copies) proves you understood rather than memorized.
- *"Input not sorted, order must be preserved"* — locality dies; you need a value→count hash map, O(n) space, same reader/writer skeleton otherwise.
- *"Values arrive as a stream, emit the kept ones"* — the algorithm is already streaming: state is just the last two emitted values; nice segue into dedup in log pipelines.
