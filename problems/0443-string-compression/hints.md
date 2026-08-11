## Hint 1

Two jobs: *measure* each maximal run, and *emit* its compressed form. Try it first into a separate list to get the encoding rules right (no digit for singles, `12` becomes `'1','2'`) — then ask what stops you from writing into `chars` itself while you read from it.

## Hint 2

Use two pointers into the same array: `read` scans runs, `write` marks where the next compressed piece lands. The emitted piece for a run (1 char + at most a few digits) is never longer than the run itself... except never at all — prove to yourself `write` can never overtake `read` once a run is fully consumed *before* emitting.

## Hint 3

Loop: remember `chars[read]`, advance `read` to the run's end, then write the character and — only if the run length is at least 2 — each digit of `str(count)` in order. Return `write`. Test mentally on `["a","b","b",...]` (single then long run) and a run of exactly 10.
