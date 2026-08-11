# Count Vowel Substrings of a String — Editorial

## 1. Pattern recognition

Two independent requirements on one substring — "only characters from this alphabet" and "all five distinct characters present" — is the classic **character-class analysis** setup (this is the duplicate/character-analysis question named in the Snowflake prep guide). The first requirement is a *segmentation* condition: a consonant anywhere kills the substring, so consonants chop the string into isolated vowel runs. The second is a *coverage* condition inside each run, and "count substrings whose window covers all required characters" is the same shape as Minimum Window Substring — solved by tracking per-character bookkeeping while sweeping an endpoint.

The interview habit worth practicing here: read the spec out loud and enumerate the token classes before coding. There are exactly two — vowels (five kinds, each individually tracked) and consonants (all equivalent: every one is a wall). That enumeration *is* the algorithm design.

## 2. Brute force first

Try all O(n²) substrings; for each, scan it and check "no consonant, and set of chars ⊇ {a,e,i,o,u}". That's O(n³), or O(n²) if you extend each substring one character at a time and maintain the set incrementally. With `n <= 100` this passes comfortably — say so out loud, then volunteer the linear version anyway: the constraints are small precisely so the interviewer can see whether you *choose* to think in counting terms rather than enumeration terms.

## 3. The key insight

**Fix the substring's right end: because extending left never loses a vowel, the valid left ends form a contiguous prefix of the current vowel run, and its length is `min(last index of each vowel) − run_start + 1`.**

## 4. Step-by-step derivation

1. Consonants are walls → process each maximal all-vowel run independently. Maintain `run_start`, resetting it to `i + 1` at every consonant.
2. Inside a run, sweep the right endpoint `i` and count valid left endpoints instead of enumerating substrings. Counting-per-endpoint is what collapses O(n²) substrings into O(n) work.
3. `word[left..i]` contains all five vowels exactly when `left <=` the last occurrence of *every* vowel — the scarcest vowel is the binding constraint. So the number of valid `left` values is `min(last_seen.values()) - run_start + 1` once all five have been seen at least once in the run.
4. Both `run_start` and the last-seen map must reset at a consonant. Forgetting to clear the map is *the* bug in this problem: a stale `last_seen['a']` from before the wall silently counts substrings that cross a consonant.
5. Each character does O(1) work (the `min` over a fixed 5-entry map is constant) → O(n) total.

## 5. Annotated Python solution

```python
class Solution:
    def countVowelSubstrings(self, word: str) -> int:
        VOWELS = frozenset("aeiou")
        total = 0
        run_start = 0        # left edge of the current all-vowel run
        last = {}            # vowel -> most recent index inside the run
        for i, ch in enumerate(word):
            if ch not in VOWELS:
                # consonant: every substring crossing i is disqualified
                run_start = i + 1
                last.clear()
                continue
            last[ch] = i
            if len(last) == 5:
                # any start in [run_start, min(last seen)] works with end = i
                total += min(last.values()) - run_start + 1
        return total
```

## 6. Complexity

- **Time O(n)** — "one pass; per character a dict update and a min over at most five entries, both constant."
- **Space O(1)** — "the map never holds more than five keys."

## 7. Edge-case traps

- **No consonants at all** — the whole string is one run; `run_start` stays 0 and the count can get large (`"aeiou" * 20` → 4656).
- **All five vowels present but split by a consonant** (`"aeiobu"`) → answer 0; this catches solutions that forget to clear `last`.
- **Repeated vowels** (`"aeeiiouua"`) — the min-of-last-seen must use the *latest* index of each vowel, not the first.
- **Four of five vowels** (`"aeio"`) → 0; the `len(last) == 5` gate must be strict.
- **Single character / all consonants** → 0, with no special-case code needed.
- An off-by-one in `min(...) - run_start + 1` halves or doubles nothing obvious on small tests — verify it on `"aeiou"` (must be exactly 1).

## 8. (DP section — not applicable)

Not DP. This trains the reusable **count-per-right-endpoint** template: sweep the right edge and count valid left edges via monotone bookkeeping — the same move that powers Subarrays with K Different Integers and the "exactly k = atMost(k) − atMost(k−1)" family.

## 9. Interviewer follow-up

- *"Now `word` can be 10⁵ long"* — nothing changes: the reference is already O(n); this question exists to check you didn't submit the O(n²) enumeration.
- *"Count substrings with all five vowels, consonants allowed"* — the wall logic disappears; keep `run_start = 0` forever and it's the same min-of-last-seen sweep.
- *"Each vowel exactly once?"* — coverage becomes an equality constraint; now both ends of the valid window are pinned, so track first-and-last occurrences or use a fixed-size sliding window of length 5 over vowel runs.
- *"Stream the characters"* — the state is five last-seen indices plus `run_start`: O(1) memory, so it streams as-is.
