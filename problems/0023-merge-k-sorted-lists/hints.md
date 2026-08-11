## Hint 1

You already know how to merge *two* sorted lists with two pointers. The question is how to scale that to k lists without comparing everything against everything. At any moment, which nodes are even candidates to be the next output node?

## Hint 2

Only the current **head of each list** can be next — k candidates, and you repeatedly need the smallest of them. "Repeatedly extract the minimum of a changing set of k things" is the textbook job description of a **min-heap**. When you extract a node, what takes its place among the candidates?

## Hint 3

Seed a heap with each non-empty list's head; pop the smallest, append it to the output (use a dummy head node), and push that node's successor if it exists. Python detail: `ListNode`s aren't comparable, so push `(val, index, node)` tuples — the index breaks value ties before Python ever compares two nodes. O(N log k) for N total nodes. The divide-and-conquer pairwise merge reaches the same bound.
