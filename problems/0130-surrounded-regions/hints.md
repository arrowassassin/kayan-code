## Hint 1

Deciding "is this region fenced in?" while flooding it is awkward — you only learn the answer after the flood finishes. Try inverting the question: which `"O"` regions are *guaranteed to survive*?

## Hint 2

A region survives exactly when it contains a border cell. So instead of flooding every region and checking, flood **only from the border `"O"` cells** — everything you reach is safe; every `"O"` you never reach is captured.

## Hint 3

Three phases: (1) multi-source BFS/DFS seeded with all border `"O"`s, relabeling reached cells with a temporary marker like `"S"`; (2) sweep the board flipping remaining `"O"` to `"X"`; (3) restore `"S"` to `"O"`. Use an explicit stack or deque — a 200x200 serpentine region overruns Python recursion — and mark cells at push time.
