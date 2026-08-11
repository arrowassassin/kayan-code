## Hint 1

This is a reader/writer two-pointer problem: one index scans every element, another marks the end of the kept prefix. The only question is the *keep test* — when does the current element deserve a slot?

## Hint 2

Because the array is sorted, "value `x` already appears twice in the kept prefix" has a beautifully local test: it's equivalent to comparing `x` against the kept element **two slots back**. No counters, no dictionaries.

## Hint 3

Keep `x` iff `write < 2 or nums[write - 2] != x`; if kept, write it at `nums[write]` and bump `write`. Compare against the *kept* prefix (`nums[write - 2]`), not the original array (`nums[read - 2]`) — the original may hold values you already skipped. Return `write`.
