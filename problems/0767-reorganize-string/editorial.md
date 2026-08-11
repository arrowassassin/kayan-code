# Reorganize String — Editorial

## 1. Pattern recognition

"Rearrange so no two equal characters touch" is Task Scheduler with the dials turned to extremes: cooldown of exactly 1 and **idle units forbidden** — every slot must hold a real character or the whole thing is impossible. Two signals mark the family: only the **frequency profile** matters (you may permute freely), and there's a **greedy-with-heap** construction where you always spend the resource under the most pressure. When a problem says "any valid answer accepted", expect to *build* a witness, not just count.

## 2. Brute force first

Try all permutations and test adjacency: O(n!) — dead on arrival past n ≈ 10. A subtler naive idea — repeatedly append any character different from the last one — is O(n·26) fast but **wrong**: on `"aaabbc"` it can happily spend `b` and `c` early (`bcab...`) and strand two `a`s with nothing to separate them. The counterexample is the point: a valid greedy must not just avoid the last character, it must prioritize the character *most in danger of getting stranded* — the one with the most copies left.

## 3. The key insight

**Always place the letter with the most remaining copies (excluding the one just placed) — and an arrangement exists at all iff the majority letter has at most ⌈n/2⌉ copies.**

## 4. Step-by-step derivation

1. Feasibility first. A letter with `f` copies needs `f-1` separators between its occurrences, and in a gap-free string of length n you can interleave at most `⌈n/2⌉` copies of one letter (positions 0, 2, 4, …). So `max_count > (n+1)//2` → return `""`. This is Task Scheduler's frame bound with zero slack.
2. Construction. At each step some letters are "live"; the risk is ending with two copies of one letter and nothing else. Spending the *most frequent* letter first keeps every letter's count at or below the ⌈remaining/2⌉ ceiling — an exchange argument shows if any completion exists, the greedy's choice also completes.
3. Mechanics: "repeatedly extract the max of a changing multiset" → max-heap of counts. Python's `heapq` is a min-heap, so store `(-count, letter)` — the negation idiom again.
4. The adjacency rule means the letter just placed is ineligible for one round. Implement with a **one-slot bench**: pop the best letter, append it, push the *previously* benched letter back, then bench the current one with its count decremented (drop it at zero). The bench is the whole trick — re-pushing immediately would let the same letter be popped twice in a row.
5. With the feasibility check up front, the heap can never present only the benched letter as sole survivor mid-run — the greedy always terminates with a full permutation. n pops at O(log 26) each → O(n log 26) = **O(n)** in practice.
6. Heap-free alternative worth knowing: sort letters by count, write the most frequent into even indices `0,2,4,…`, continue with the rest into remaining even then odd indices. Same feasibility condition, pure indexing.

## 5. Annotated Python solution

```python
import heapq
from collections import Counter


class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        # ceil(n/2) copies max: more and the separators run out.
        if max(counts.values()) > (len(s) + 1) // 2:
            return ""

        # Max-heap via negated counts (heapq is min-only).
        heap = [(-c, ch) for ch, c in counts.items()]
        heapq.heapify(heap)                  # O(26)

        out = []
        prev = None                          # benched letter: just used, one-round timeout
        while heap:
            negc, ch = heapq.heappop(heap)   # most copies left among eligible letters
            out.append(ch)
            if prev:                         # bench released AFTER the pop:
                heapq.heappush(heap, prev)   # guarantees ch != next pick
            prev = (negc + 1, ch) if negc + 1 else None   # negc+1 == 0 -> exhausted
        return "".join(out)
```

## 6. Complexity

- **Time O(n log a)** with alphabet size a = 26 — "n heap operations on a heap that never holds more than 26 entries — effectively linear."
- **Space O(a)** for counts and heap, **O(n)** for the output — "the working state is bounded by the alphabet, not the input."

## 7. Edge-case traps

- **Exactly-half majorities**: `"aab"` (2 of 3) is feasible, `"aa"` (2 of 2) is not — the boundary is `(n+1)//2`, and using `n//2` or strict `<` breaks one of the two.
- **Single character** `"a"` — feasible, must return `"a"`, and the loop must handle a heap that starts with one entry.
- **Pushing the used letter straight back** instead of benching it — produces `"aabb..."`-style output; the bench (release *after* the next pop) is load-bearing.
- **Forgetting to drop exhausted letters** — a zero-count bench entry re-enters the heap and emits ghost characters, corrupting the permutation.
- **Two letters, equal counts, large n** (`a^50000 b^50000`) — stresses that the loop is O(n log a), not quadratic string concatenation; build a list and join.

## 8. Reusable template

Not DP. This trains the **greedy max-heap with a cooldown bench** — spend the most-constrained resource first, holding just-used items out for one round — the identical engine behind Task Scheduler's simulation and Rearrange String k Distance Apart (with a k-slot bench queue).

## 9. Interviewer follow-up

- *"Generalize to: equal characters at least k apart"* — same greedy, but the bench becomes a FIFO queue of the last k-1 used letters (LC 358); feasibility check generalizes from the ⌈n/2⌉ bound.
- *"Why is the greedy safe?"* — be ready with the exchange argument: swapping any valid schedule's next choice for the greedy's max-count letter never destroys completability.
- *"Return the count of valid arrangements instead"* — completely different problem (combinatorics/inclusion–exclusion); recognizing that construction ≠ counting is part of the answer.
- *"Do it without the heap"* — the even/odd index-filling construction: sort by frequency, fill positions 0,2,4,… then 1,3,5,…; O(n) with no priority queue at all.
