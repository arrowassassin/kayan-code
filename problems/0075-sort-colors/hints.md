## Hint 1

Only three distinct values exist. A two-pass answer — count the 0s, 1s and 2s, then overwrite the array — is easy and worth having in your pocket. The interviewer will then ask for one pass; think about growing sorted zones at both ends of the array.

## Hint 2

Maintain three pointers partitioning the array into four zones: confirmed `0`s on the far left (`lo`), confirmed `1`s next (up to `mid`), unexamined values in the middle, and confirmed `2`s on the far right (past `hi`). Each step looks only at `nums[mid]` and shrinks the unknown zone by one.

## Hint 3

If `nums[mid]` is `1`, just advance `mid`. If it's `0`, swap with `lo` and advance **both** — the value swapped in came from the 1-zone, already examined. If it's `2`, swap with `hi` and retreat `hi` but do **not** advance `mid` — the value that arrived from the right has never been looked at. Loop while `mid <= hi` (inclusive!).
