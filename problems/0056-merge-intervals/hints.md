## Hint 1

In arbitrary order, deciding which intervals belong together seems to require comparing every pair. What single preprocessing step would guarantee that intervals belonging to the same merged group sit next to each other?

## Hint 2

After sorting by **start**, an interval can only merge with the group immediately before it — if it doesn't reach back to that group, nothing later will bridge the gap either. So one running "current merged interval" is all the state you need.

## Hint 3

Sort by start, seed the output with the first interval, then scan: if the next interval's start is `<=` the end of the last merged interval, extend that end with `max(...)`; otherwise start a fresh interval. The `<=` (not `<`) is what makes touching endpoints like `[1,4],[4,5]` collapse. Watch out: a nested interval must not *shrink* the end — that's why it's `max`, not assignment.
