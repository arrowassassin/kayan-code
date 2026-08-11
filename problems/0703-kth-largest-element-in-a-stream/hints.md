## Hint 1

You only ever report the k-th largest — nothing below it is ever the answer, and nothing below it can ever *become* the answer as more values arrive. How much of the stream do you actually need to keep?

## Hint 2

Keep exactly the k largest values seen so far. When a new value arrives, it either belongs in that elite set (pushing the weakest member out) or it doesn't matter at all. Which single member of the set do you compare against — and which data structure hands you that member in O(1)?

## Hint 3

Use a **min-heap** capped at size k: its root is the smallest of the k largest, i.e. exactly the k-th largest. On `add`, if the heap is short push; else if `val > heap[0]`, pop-and-push (`heapreplace`); return `heap[0]`. Build the initial heap from `nums` and pop it down to size k.
