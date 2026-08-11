# Reorder Data in Log Files — Editorial

## 1. Pattern recognition

The statement is a bundle of *ordering rules*, not an algorithmic puzzle: a two-tier partition (letter before digit), a compound comparison inside one tier (content, then identifier), and a **preserve-input-order** requirement in the other. Whenever a problem hands you layered ordering rules, the pattern is **custom sort key + stability** — translate each English rule into one component of a key tuple and let the library sort do the work. The parsing habit applies to specs, not just strings: read each rule aloud and ask "which key component encodes this?" If a rule maps to no component, you've missed something — here, rule 3 maps not to the key but to the *stability guarantee* of the sort.

## 2. Brute force first

The manual route: partition into two lists, sort the letter-logs with a hand-written comparator (or `functools.cmp_to_key`), concatenate, leaving digit-logs untouched. It's O(n log n · L) too, and perfectly acceptable — but it's three steps of bookkeeping where one `sorted(..., key=...)` call suffices, and hand-written comparators are where bugs breed (asymmetric compares, forgotten tie-breaks). The genuinely *wrong* route is sorting digit-logs too, or re-splitting each log inside a comparator called O(n log n) times.

## 3. The key insight

**Give every log a tuple key — `(0, content, identifier)` for letter-logs, a constant `(1,)` for digit-logs — and let sort stability keep equal-keyed digit-logs in their original order.**

## 4. Step-by-step derivation

1. Parse each log exactly once: `ident, rest = log.split(" ", 1)` — `maxsplit=1` is the load-bearing detail, since content itself contains spaces and must stay intact for comparison.
2. Classify by `rest[0].isdigit()`. Only the first content character is needed: the problem guarantees a log is entirely one flavor, and the identifier (which may contain digits — `"a1"`, `"let1"`) must play no part in classification.
3. Encode rule 1 in the tuple's first slot: 0 for letter-logs, 1 for digit-logs — tuples compare component-wise, so every `(0, ...)` precedes every `(1,)`.
4. Encode rule 2 in the remaining slots: `(0, rest, ident)` gives content-first, identifier-tiebreak ordering for free. Note the whole content string compares as one unit — `"m w" < "mo"` because space (0x20) sorts before every letter; don't "normalize" it away.
5. Encode rule 3 by *omission*: all digit-logs share the identical key `(1,)`, and Python's `sorted` is documented as **stable** — ties keep input order. Saying the word "stable" out loud is the point of this problem; without that guarantee the one-liner would be wrong.

## 5. Annotated Python solution

```python
class Solution:
    def reorderLogFiles(self, logs: list[str]) -> list[str]:
        def sort_key(log: str):
            ident, rest = log.split(" ", 1)
            if rest[0].isdigit():
                return (1,)              # all digit-logs share one key -> stable order kept
            return (0, rest, ident)      # letter-logs: content first, identifier breaks ties
        return sorted(logs, key=sort_key)   # sorted() is stable — that IS the algorithm
```

## 6. Complexity

- **Time O(n log n · L)** — "the sort makes O(n log n) comparisons and each comparison touches strings of length up to L; keys are computed once per log, not per comparison."
- **Space O(n · L)** — "the key tuples and the sorted output."

## 7. Edge-case traps

- **Digit-log relative order** — the whole reason `(1,)` is constant; keying digit-logs by their content silently reorders them and passes small tests.
- **Identifiers containing digits** (`"let1 art can"`, `"5 m w"`) — flavor comes from *content*, never the identifier; `"5 m w"` is a letter-log.
- **Identical content, different identifiers** (`"l5 act act"` vs `"l2 act act"`) — the third tuple slot must exist or the order is unspecified.
- **Content with spaces comparing as a unit** — `"m w" < "mo"`; joining/splitting content tokens changes the ordering.
- **`split(" ", 1)` vs `split()`** — full splitting then rejoining risks collapsing the exact byte content being compared.
- **All-digit or all-letter inputs** — one tier empty; the key approach needs no special case.

## 8. (DP section — not applicable)

Not DP. This trains the **decorate-with-a-tuple-key + rely-on-stability** template — the same move behind Top K Frequent Words' `(-count, word)` key and every "sort by A, then B, keep input order for ties" requirement.

## 9. Interviewer follow-up

- *"Digit-logs should sort by numeric value now"* — replace `(1,)` with `(1, [int(t) for t in rest.split()])`; the framework absorbs rule changes by editing one key line, which is the argument for keys over comparators.
- *"Logs arrive as a stream; letter-logs must be emitted sorted so far"* — a sorted container (or heap) for letter-logs, a plain queue for digit-logs; stability becomes explicit FIFO.
- *"Why is Python's sort stable, and does it cost anything?"* — Timsort guarantees it; stability is free here and is precisely what merge-based sorts give you. Knowing which library guarantees you're leaning on — and that e.g. C++ `std::sort` does *not* promise stability (`std::stable_sort` does) — is the senior-level takeaway.
- *"Millions of logs"* — key computation is the linear part; discuss sorting cost vs a single partition pass when only rule 1 matters.
