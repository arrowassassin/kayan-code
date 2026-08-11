## Hint 1

"Shortest contiguous window covering a requirement" is a sliding-window problem — the same two-pointer skeleton as Longest Substring Without Repeating Characters, but the roles flip: there you shrank when the window went *bad*; here you shrink while the window is *good*, recording the best length as you go.

## Hint 2

Track coverage with a count map built from `t`, letting counts go **negative** for surplus copies. The expensive part is knowing whether the whole requirement is met without scanning the map each step — maintain a single integer `missing` (characters still required, with multiplicity) and update it only when a count crosses zero.

## Hint 3

For each `right`: decrement `need[s[right]]`, and if it was positive beforehand, decrement `missing`. While `missing == 0`, the window is valid — record it if shorter than the best, then advance `left`, incrementing `need[s[left]]` and bumping `missing` back up if that count becomes positive. Store the best window as (start, length) — don't slice the string inside the loop.
