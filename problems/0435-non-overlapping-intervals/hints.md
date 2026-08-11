## Hint 1

"Remove the fewest" is the same question as "keep the most non-overlapping intervals" — a scheduling/selection problem, not a merging one. That reframing changes which sort key is right.

## Hint 2

Among all intervals you could keep next, the one that **ends earliest** leaves the most room for everything after it — choosing it can never be worse than choosing a longer one. That's the greedy exchange argument.

## Hint 3

Sort by **end**. Scan, remembering the end of the last interval you kept. If the next interval starts at or after that end (touching is fine here), keep it and update the end; otherwise count it as removed. Answer = total − kept. One removal counter, no rebuilding of lists.
