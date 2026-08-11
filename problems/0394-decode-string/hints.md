## Hint 1

Nesting is the whole problem: when you meet `3[a2[c]]`, you can't finish the outer block until the inner one is done. "Suspend what I'm doing, handle the inner thing, come back" — which data structure gives you that for free?

## Hint 2

Walk the string once, maintaining two pieces of state: the string being built at the **current** nesting depth, and the number being accumulated digit by digit (careful: `12[` arrives as `'1'` then `'2'`). On `[`, push both onto a stack and start fresh; on `]`, pop to recover the outer context.

## Hint 3

On `]`: pop `(outer_string, k)`, and set current = `outer_string + current * k`. At the end of the scan the stack is empty and the current string is the answer. Collect pieces in a list and join — repeated string concatenation inside deep nesting turns quadratic.
