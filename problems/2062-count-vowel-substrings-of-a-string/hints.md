## Hint 1

A consonant is a hard wall: no qualifying substring can cross it. So the string splits into independent all-vowel runs, and you only ever count inside one run at a time. With `n <= 100`, even checking every substring with a set is fine — but the interviewer will want the linear idea.

## Hint 2

Fix the right endpoint `i` inside a vowel run and ask: how many left endpoints make `word[left..i]` contain all five vowels? Adding characters to the left never *removes* a vowel, so the valid left endpoints form a prefix of the run — you only need to know where that prefix ends.

## Hint 3

Track, for each of the five vowels, the **most recent index** where it appeared in the current run. Once all five have been seen, every start position from the run's beginning up to `min(last_seen)` works, so add `min(last_seen) - run_start + 1` for this endpoint. Reset both the run start and the last-seen map whenever you hit a consonant.
