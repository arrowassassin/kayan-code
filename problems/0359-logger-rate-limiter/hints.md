## Hint 1

You never need the history of when a message was printed — only whether it may print *now*. What single fact per message answers that question?

## Hint 2

Store, per message, the earliest timestamp at which it is allowed to print again. A new call compares `timestamp` against that stored value: one dict lookup, one comparison. Be careful which calls update the stored value.

## Hint 3

`if timestamp < next_ok.get(message, 0): return False` — otherwise set `next_ok[message] = timestamp + 10` and return `True`. Only a *printed* message resets its timer; a rejected duplicate must leave the entry untouched. Check the boundary: arriving exactly 10 seconds later prints, so the test is `<`, not `<=`.
