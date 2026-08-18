# Problem Authoring Spec (KayanCode)

Every problem is a folder `problems/<slug>/` with EXACTLY these files:
`problem.md`, `meta.json`, `starter.py`, `solution.py`, `tests.json`, `hints.md`, `editorial.md`.

**Study the exemplars first**: `problems/0057-insert-interval/` (function mode)
and `problems/0146-lru-cache/` (methods/design mode). Match their tone, depth
and structure exactly.

**Verification is mandatory**: after authoring, run
`python3 scripts/verify_bank.py <your-slug-prefixes>` and fix everything it
reports. The ONLY acceptable remaining errors are `follow_up`/`follow_up_of`
links pointing at problems another agent is authoring (cross-topic links).
Your reference `solution.py` MUST get AC on your own full hidden suite via the
real judge — that's what the script checks.

## Slugs

`<4-digit-zero-padded-id>-<kebab-title>`, e.g. `0994-rotting-oranges`,
`1235-maximum-profit-in-job-scheduling`.

## problem.md

Original statement **in your own words** (do NOT copy LeetCode text) with:
title heading, statement, 1–3 worked examples in fenced blocks, `## Constraints`
section. Clarity + edge-case-relevant constraints matter (they feed the mock
interview clarify gate).

## meta.json

```json
{
  "id": 994,
  "title": "Rotting Oranges",
  "difficulty": "Medium",            // Easy | Medium | Hard
  "topics": ["Graph BFS/DFS"],       // EXACT canonical topic names, usually 1
  "priority": 2,                     // 1 = ★ frequently-reported/named, 2 = core-topic, 3 = pattern support
  "follow_up": "<slug>",             // optional: harder linked extension
  "follow_up_of": "<slug>",          // optional: the warmup this extends
  "judge": { ... }                   // see below
}
```

Canonical topic names (use EXACTLY): `Graph BFS/DFS`, `Trees`,
`String Parsing`, `Top-K / Heap`, `Sliding Window`, `Two Pointer`,
`Dynamic Programming`, `Intervals`, `Stream / Design`.

## judge config

Function problems (`class Solution` with one entry method, LeetCode camelCase):
```json
{ "mode": "function", "entry": "orangesRotting", "compare": "exact" }
```
Options:
- `compare`: `exact` (default; bool≠int, int==float, floats to 1e-6) |
  `unordered` (top-level list as multiset — e.g. results in any order) |
  `unordered_2d` (inner lists sorted then outer as multiset — 3Sum, Group Anagrams) |
  `float` (recursive tolerance 1e-6 — Median of Data Stream)
- `arg_types`: per-argument conversions, e.g. `["tree"]`, `["listnode[]", "raw"]`.
  Types: `raw` (default), `tree` (level-order array w/ nulls → TreeNode),
  `listnode` (array → ListNode), `listnode[]`, `graph` (LC-133 adjacency list
  → Node with 1-indexed vals). `TreeNode`/`ListNode`/`Node` classes are
  pre-defined in the judge namespace — starter.py references them in type
  hints WITHOUT defining or importing them (add a comment
  `# TreeNode is predefined: val/left/right`).
- `ret_type`: `raw` | `tree` | `listnode` | `graph` (converts return back to
  arrays for comparison).
- `compare_arg`: integer — compare this (mutated) argument instead of the
  return value (in-place problems like Sort Colors).
- `time_limit`: seconds per test, default 3.0 — leave default.

Design problems:
```json
{ "mode": "methods", "entry": "LRUCache", "compare": "exact" }
```
Test input is `[ops, args]` (LeetCode style), expected is the output list with
`null` for constructor/void. A single expected slot may be
`{"$anyOf": [a, b]}` when several answers are valid (e.g. `getRandom`).

Problems with many valid outputs (Reorganize String, Longest Palindromic
Substring, in-place k-return problems like Remove Duplicates II / String
Compression): add a `checker.py` file:
```python
def check(args_after, returned, expected):
    # return True/False, or (False, "note shown to the user")
    ...
```
`args_after` = the argument list after the call (mutations visible; tree/list
args are converted back to arrays). Design the `expected` value to carry
whatever the checker needs (e.g. the required length).

Special case — Serialize/Deserialize (297): judge is
`{"mode":"function","entry":"roundtrip","arg_types":["tree"],"ret_type":"tree"}`;
starter defines `class Codec` (the part the user writes) plus a DO-NOT-EDIT
`class Solution` whose `roundtrip(root)` does
`codec.deserialize(codec.serialize(root))`.

LCA-style problems: pass p/q as plain **values** (state in problem.md that all
node values are unique and p/q are given as values).

## tests.json

```json
{ "visible": [ {"input": [...args], "expected": ...}, ... ],
  "hidden":  [ ... ] }
```
- ≥ 2 visible (the examples from problem.md — they're user-editable in the UI;
  plain JSON only).
- ≥ 6 hidden covering: empty/minimal input, single element, duplicates,
  boundary constraint values, the trap the follow-up targets, and where
  meaningful ONE stress test big enough that an obvious brute force would TLE
  (3s) but the reference passes easily. For large cases use
  `"input_py": "<python expr for the args list>"` and
  `"expected_py"`/`"expected"` (hidden only), e.g.
  `{"input_py": "[list(range(100000))]", "expected": 100000}`.

## starter.py

LeetCode-style stub: `class Solution:` + typed entry method + `pass` (or the
design class with method stubs). No solution logic, no imports the user must
keep.

## solution.py

The interview-ready reference solution — IDENTICAL to the annotated solution
in editorial.md (minus the annotations is fine, but same algorithm). It must
pass the full suite under the judge.

## hints.md

Exactly 3 progressive hints, each under a `## Hint N` heading: 1 = nudge at
the pattern, 2 = the key structural observation, 3 = nearly the approach,
stopping short of code.

## editorial.md — the 9-part expert track (verify checks the markers)

```
# <Title> — Editorial
## 1. Pattern recognition       <- what in the STATEMENT signals the technique
## 2. Brute force first         <- sketch, complexity, exactly why constraints kill it
## 3. The key insight           <- ONE sentence, bolded
## 4. Step-by-step derivation   <- brute force → optimal, each step answers WHY
## 5. Annotated Python solution <- interview-ready, comments at decision points only
## 6. Complexity                <- time+space with the one-line SPOKEN justification in quotes
## 7. Edge-case traps           <- the inputs the follow-up will target
## 8. (DP problems only) Top-down AND bottom-up + the mechanical conversion recipe
      (non-DP: one line saying which reusable template this problem trains)
## 9. Interviewer follow-up     <- likely extension + how to adapt
```
DP problems MUST show both memoized top-down and iterative bottom-up code and
the mechanical conversion recipe (state → params, memo → table, recursion
order → loop order, base case → init).

Quality bar: teach the WHY. Write like a great human coach, not a summary.
250–600 words of prose beyond the code. Never copy LeetCode editorial text.

## Linked warmup→extension pairs (set BOTH sides' meta fields)

- 0056-merge-intervals → 0057-insert-interval → 0759-employee-free-time (57 done)
- 0003-longest-substring-without-repeating-characters → 0076-minimum-window-substring
- 0198-house-robber → 1235-maximum-profit-in-job-scheduling
- 0102-binary-tree-level-order-traversal → 0103-binary-tree-zigzag-level-order-traversal
- 0215-kth-largest-element-in-an-array → 0347-top-k-frequent-elements
- 0200-number-of-islands → 0994-rotting-oranges (200 done)
- 0146-lru-cache → 0380-insert-delete-getrandom (146 done)
- 0207-course-schedule → 0210-course-schedule-ii
- 0130-surrounded-regions → 0417-pacific-atlantic-water-flow
- 0543-diameter-of-binary-tree → 0437-path-sum-iii
- 0199-binary-tree-right-side-view → 0987-vertical-order-traversal-of-a-binary-tree
- 0394-decode-string → 0227-basic-calculator-ii
- 0125-valid-palindrome → 0680-valid-palindrome-ii
- 0347-top-k-frequent-elements → 0692-top-k-frequent-words
- 0023-merge-k-sorted-lists → 0295-find-median-from-data-stream
- 0904-fruit-into-baskets → 0992-subarrays-with-k-different-integers
- 0167-two-sum-ii → 0015-3sum
- 0011-container-with-most-water → 0042-trapping-rain-water
- 0062-unique-paths → 1143-longest-common-subsequence
- 0139-word-break → 0091-decode-ways
- 0435-non-overlapping-intervals → 0253-meeting-rooms-ii
- 0346-moving-average-from-data-stream → 0362-design-hit-counter
- 0359-logger-rate-limiter → 0703-kth-largest-element-in-a-stream
