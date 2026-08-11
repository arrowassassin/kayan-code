## Hint 1

Don't process the path character by character — split it on `/` first. After splitting, every piece is one of exactly four kinds: empty (from repeated or edge slashes), `.`, `..`, or a real name. Enumerate what each kind should *do*.

## Hint 2

`..` undoes the most recently entered directory — "undo the most recent thing" is the signature of a **stack**. Real names push; `..` pops (if there's anything to pop); `.` and empty pieces are no-ops.

## Hint 3

After the scan, the stack holds the canonical directory chain from root outward. Build the answer as `"/" + "/".join(stack)` — this single expression handles the empty-stack case (root) and guarantees no trailing slash. Make sure `..` on an empty stack is silently ignored, not an error.
