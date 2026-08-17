## Hint 1

A hash set of words answers `search` in O(1) — but how would it answer `startsWith` without scanning every stored word? The structure you want shares work between words that share a beginning.

## Hint 2

Picture a tree where each **edge** is one letter: every stored word is a root-to-somewhere path, and words with a common prefix share that path. In Python the lightest node is just a dict mapping letter → child node — no class needed. Both queries become "walk the path letter by letter; fail on a missing edge."

## Hint 3

`search` and `startsWith` walk identically — the only difference is what they check at the end. Reaching the last node proves the *prefix* exists, but not that a word *ends* there ("app" vs "apple"). Plant an end-of-word marker (a sentinel key like `"$"`) at the final node of every insert; `search` additionally demands the marker, `startsWith` doesn't.
