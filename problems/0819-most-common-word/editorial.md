# Most Common Word — Editorial

## 1. Pattern recognition

A frequency question (`most common`, `count`) wrapped in a **normalization gauntlet**: case folding, punctuation stripping, a stop-list. That combination — normalize, tokenize, count, argmax — is the word-count pipeline, the "hello world" of text processing, and the interview points are almost entirely in the tokenization. Read the spec aloud and enumerate the token classes before coding: letters (accumulate, lowercased), everything else (flush the current word). Two classes. Notice what that implies: punctuation doesn't just trail words — `"x!x!!x"` is *three* words, and an apostrophe splits `"can't"` into `can` and `t`. Candidates who assume `split()` is enough miss exactly these.

## 2. Brute force first

There's no asymptotic trap — the input is 1,000 characters. The brute-force axis is *robustness*: `paragraph.split()` then `.strip(punctuation)` per token handles `"ball,"` but silently mishandles interior punctuation (`"x!x"` stays one token). A per-character re-scan of the banned list instead of a set lookup is O(words × banned) — harmless here, but say "set" anyway; it's free. The pragmatic Python answer is one line of regex — `re.findall(r"[a-z]+", paragraph.lower())` — and it is genuinely correct because the character class *is* the token definition. Offer it, then show you can write the scan by hand; the manual state machine is what transfers to languages without `re` and to streaming input.

## 3. The key insight

**A word is a maximal run of letters — treat every non-letter as a flush point, lowercase while accumulating, and count only words outside the banned set.**

## 4. Step-by-step derivation

1. Tokenizer as a two-state machine: "inside a word" (buffer non-empty) vs "between words". A letter appends `ch.lower()` to the buffer; any other character, if the buffer is non-empty, emits the buffered word and clears it.
2. The end-of-input flush is the off-by-one trap: `"a."` flushes on `.`, but `"one"` ends mid-word. Appending a sentinel non-letter (`paragraph + "."`) makes the loop's own flush logic handle the last word — one rule, zero special cases after the loop.
3. Banned filtering happens at emit time against a `set` (O(1) membership). Filtering *before* lowercasing is a bug — the banned list is lowercase, the text isn't.
4. Count with a dict and track the running argmax during the same pass; the uniqueness guarantee means "strictly greater" is a safe update rule and no tie-break policy is needed.
5. Total: one pass over the characters, one dict — nothing to optimize further.

## 5. Annotated Python solution

```python
class Solution:
    def mostCommonWord(self, paragraph: str, banned: list[str]) -> str:
        banned_set = set(banned)
        counts = {}
        best, best_count = "", 0
        word = []
        # sentinel "." guarantees the last word gets flushed
        for ch in paragraph + ".":
            if ch.isalpha():
                word.append(ch.lower())          # normalize case as we read
            elif word:
                w = "".join(word)
                word = []
                if w not in banned_set:
                    c = counts.get(w, 0) + 1
                    counts[w] = c
                    if c > best_count:
                        best, best_count = w, c
        return best
```

## 6. Complexity

- **Time O(n + b)** — "one pass over the paragraph, constant work per character; building the banned set is linear in its size."
- **Space O(n + b)** — "the counts dict and banned set; the word buffer is bounded by the longest word."

## 7. Edge-case traps

- **Interior punctuation** (`"x!x!!x"`) — three separate words, not one; the flush-on-non-letter rule handles it, `split()` does not.
- **Apostrophes** (`"can't"` → `can`, `t`) — per the spec `'` is a separator; don't "helpfully" keep contractions together.
- **The unflushed final word** (`"one"`, `"a a b b a"`) — the sentinel exists for this.
- **Case-crossing counts** (`"ball,"` + `"BALL"` = 2) — lowercase at accumulation time, once.
- **Banned words dominating the text** — they must be excluded from counting, not subtracted later.
- **Punctuation runs** (`"such...parsing"`) — consecutive separators must not emit empty words; the `elif word:` guard is that check.

## 8. (DP section — not applicable)

Not DP. This trains the **buffered tokenizer with sentinel flush** — the same accumulate/flush state machine as Reverse Words and String Compression, plus a normalize-then-count tail.

## 9. Interviewer follow-up

- *"Top k words instead of the single best"* — keep the counting pass, then a heap of size k over the counts (Top K Frequent Words 692); discuss tie-breaking, which the uniqueness guarantee let us skip here.
- *"Gigabytes of text"* — the tokenizer is already streaming (O(1) state per character); the counts dict is the memory problem — shard by hash of the word, or approximate with count-min sketch. Distinguishing "tokenizer scales, counter doesn't" is the senior answer.
- *"Unicode text"* — `isalpha()` and `lower()` get more interesting (locale, casefold); the token-class *definition* is the part that changes, the machine doesn't.
- *"Banned list is huge"* — it's already a set; mention bloom filters if it must live off-heap.
