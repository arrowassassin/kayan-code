## Hint 1

Only letter counts matter, not positions. Start with feasibility: if one letter makes up more than half of the string (rounded up), can any arrangement keep its copies apart? Work out the exact threshold before thinking about construction.

## Hint 2

To avoid painting yourself into a corner, spend the letter with the **most remaining copies** at every step — it's the one whose deadline is tightest. The only restriction: it can't be the letter you just placed. That's "repeatedly pick the max of a changing set, with one element temporarily off-limits" — a max-heap plus a one-slot bench.

## Hint 3

Push `(-count, letter)` pairs into a heap. Loop: pop the best available letter, append it, *then* return the previously benched letter to the heap, and bench the one you just used (with its count decremented, dropping it when it hits zero). With the feasibility check `max_count <= (len(s)+1)//2` done up front, this greedy never gets stuck. (Alternative: fill even indices `0,2,4,...` with the most frequent letter first, then odd indices — no heap at all.)
