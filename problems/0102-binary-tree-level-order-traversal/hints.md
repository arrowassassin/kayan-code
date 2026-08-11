## Hint 1

You need nodes in order of distance from the root. Which of the two standard traversals — depth-first or breadth-first — visits nodes in exactly that order for free?

## Hint 2

A plain BFS queue gives you the right *order* but not the *grouping*: nodes from two adjacent levels coexist in the queue. What quantity, captured at the right moment, tells you where one level ends and the next begins?

## Hint 3

At the top of each outer loop iteration, the queue holds exactly one complete level. Snapshot `len(queue)`, pop exactly that many nodes into one output list while pushing their children, and repeat. (A DFS carrying a `depth` parameter that appends to `result[depth]` also works — say why you chose yours.)
