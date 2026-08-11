# Surrounded Regions — Editorial

## 1. Pattern recognition

Grid, 4-directional regions, flood-fill vocabulary — clearly the Number of Islands family. The distinguishing feature is the *condition* attached to each region: "captured unless it touches the border". Conditions of the form "keep whatever is connected to a special boundary set" are a cue to run the traversal **from the boundary inward** rather than from each region outward. That inversion — solve for the survivors, complement for the captured — is the exact move this problem exists to teach, and the one its follow-up (Pacific Atlantic) escalates.

## 2. Brute force first

The direct simulation: for each unvisited `"O"`, flood its whole region while watching whether any cell lies on the border; afterwards, if it never touched the border, walk the region *again* to flip it (or buffer the cells). Complexity is still O(mn) — the real costs are code complexity and bug surface: you must collect every region's cell list (O(mn) extra memory), track a "touched border" flag through the flood, and do a second pass per region. It's acceptable, but the interviewer is waiting for you to notice that the flag is knowable *in advance*: regions containing a border cell survive, all others don't — so start where the answer is already known.

## 3. The key insight

**Flood from the border "O" cells only: everything reached is provably safe, and every "O" left unreached is captured by definition — no per-region bookkeeping at all.**

## 4. Step-by-step derivation

1. A region survives iff it contains a border cell (that *is* the capture rule, restated). Reachability from the border along `"O"` cells identifies exactly the surviving cells.
2. Seed a queue with every `"O"` on the four edges — a multi-source flood, same trick as Rotting Oranges. Relabel each reached cell `"S"` immediately at enqueue time; the relabel doubles as the visited set, so no auxiliary structure is needed.
3. Walk the queue with a `deque` (or explicit stack — no distances are needed, so BFS/DFS are interchangeable). Recursion is the wrong default here: a 200×200 board can host a 40,000-cell serpentine region, well past Python's default recursion depth. Saying that unprompted is exactly the "recursion limits" narration interviewers reward.
4. Final sweep in one pass: `"O"` → `"X"` (never rescued → captured), `"S"` → `"O"` (rescued → restored). Order within the sweep is safe because the two rewrites touch disjoint labels.
5. Total: every cell enqueued at most once, swept twice → O(mn), O(1) extra space beyond the queue.

## 5. Annotated Python solution

```python
from collections import deque


class Solution:
    def solve(self, board: list[list[str]]) -> None:
        rows, cols = len(board), len(board[0])

        # 1) flood from every border "O": those regions can escape.
        queue = deque()
        for r in range(rows):
            for c in (0, cols - 1):
                if board[r][c] == "O":
                    board[r][c] = "S"       # S = safe
                    queue.append((r, c))
        for c in range(cols):
            for r in (0, rows - 1):
                if board[r][c] == "O":
                    board[r][c] = "S"
                    queue.append((r, c))

        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                    board[nr][nc] = "S"     # mark on enqueue
                    queue.append((nr, nc))

        # 2) one sweep: unreached "O" is captured, "S" is restored.
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "S":
                    board[r][c] = "O"
```

## 6. Complexity

- **Time O(m·n)** — "each cell enters the flood at most once and the final sweep is one more linear pass."
- **Space O(m·n)** worst case for the queue — "the board itself stores the visited marks, so no extra visited structure."

## 7. Edge-case traps

- **Border `"O"`s themselves** must survive — seeding must relabel them, not just their inner neighbors; `[["O"]]` is the minimal check.
- **All-`"O"` board** → nothing flips; a version that floods regions outward and forgets the border flag flips everything.
- **1-wide boards** — every cell is a border cell; the two seeding loops visit corners twice, which the `"S"` relabel makes harmless (visited-on-mark discipline again).
- **Region touching the border only at a corner-adjacent diagonal** — diagonals do *not* connect; such a region is still captured. Clarify 4- vs 8-connectivity before coding.
- **Deep serpentine region** — the stress case; recursive DFS dies with `RecursionError` where the deque shrugs.

## 8. Reusable template

Not DP. This trains the **border-seeded inverse flood-fill template** — mark what provably survives from the boundary, complement the rest; reused directly in Pacific Atlantic Water Flow (the linked follow-up) and Number of Enclaves.

## 9. Interviewer follow-up

- *"Now cells drain to two oceans on opposite corners — which cells reach both?"* — Pacific Atlantic Water Flow (417), the linked extension: two border-seeded floods with the comparison rule generalized, then a set intersection.
- *"Board too large for O(mn) queue memory?"* — process row-band by row-band with Union-Find joining `"O"` cells to a virtual "border" node; only two rows of parent state needed at a time.
- *"Count captured regions instead of flipping"* — same flood, then component-count the leftover `"O"`s with the standard sweep; or run Union-Find with a virtual escape node and count roots not attached to it.
