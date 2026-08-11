## Hint 1

Simulating water flowing *out* of every cell means one traversal per cell — expensive. Try inverting the question: instead of "which cells can reach ocean X?", ask "starting from ocean X, which cells can water arrive *from*?"

## Hint 2

Reverse the flow rule. Water flows downhill-or-level outward, so walking *inland from the ocean border* you may step onto a neighbor whose height is **greater than or equal to** yours. One traversal seeded with the entire Pacific border finds every Pacific-draining cell; one more for the Atlantic.

## Hint 3

Run two multi-source BFS/DFS passes (all top+left border cells for the Pacific, all bottom+right for the Atlantic), each collecting a visited set of reachable cells. The answer is the intersection of the two sets. Mind the comparison direction (`neighbor >= current` when walking inland) and add cells to the visited set when enqueuing, not when popping.
