## Hint 1

Strip away the zigzag for a second: what remains is plain level-order traversal. Solve that first — the alternation should be a decoration, not a redesign.

## Hint 2

The set of nodes per level is identical to ordinary level order; only the *presentation* of every second level changes. So where is the cheapest place to apply the direction — while traversing, or after a level is complete?

## Hint 3

Run the standard BFS level loop (snapshot `len(queue)`, pop exactly that many). Keep a boolean that flips after each level; append `level` as-is or reversed depending on it. Resist mutating the queue order itself — that corrupts which children get discovered when.
