# Valid Palindrome II — Editorial

## 1. Pattern recognition

"Palindrome" is already a two-pointer word — compare mirrored positions from the outside in. The twist is the **one-deletion budget**, and the pattern to recognize is *two pointers plus a bounded branch*: run the ordinary check, and when it first disagrees, the tiny budget means only a constant number of repair options exist. Problems that grant "at most one edit" (delete here; substitute in Valid Palindrome III's cousin; one swap elsewhere) almost always resolve this way: the scan pins down where the edit must happen, then you try each option.

## 2. Brute force first

For each of the `n` positions, delete that character and test the remainder: O(n) deletions × O(n) check = **O(n²)**, and slicing (`s[:i] + s[i+1:]`) adds an O(n) copy per attempt. At `n = 10^5` a near-palindrome that fails deep in the middle forces ~10⁹–10¹⁰ character comparisons — dead. The waste is obvious once said aloud: deleting a character at position 3 cannot possibly fix a mismatch the check only reaches at position 40,000.

## 3. The key insight

**At the first mismatch `s[i] != s[j]`, everything outside the window `[i, j]` is already verified — so a single deletion can only succeed by removing `s[i]` or `s[j]`, leaving exactly two candidate windows to check.**

## 4. Step-by-step derivation

1. Run the standard scan: `i` from the left, `j` from the right, advancing while `s[i] == s[j]`. If the pointers cross, `s` is already a palindrome — `True`, budget unspent.
2. Suppose the scan stops at the first mismatch. Why must the deleted character be one of the two mismatching ends? Deleting any character *outside* `[i, j]` breaks a pair that already matched (its mirror partner shifts by one against an unshifted half) and does nothing to fix `s[i]` vs `s[j]`. Deleting a character *strictly inside* `(i, j)` leaves both `s[i]` and `s[j]` in place, still mirrored against each other, still unequal. That exhausts every option except deleting `s[i]` or `s[j]` — the "why can you skip all other deletions?" answer an interviewer wants stated, not waved at.
3. So the answer is `is_pal(i+1, j) or is_pal(i, j-1)` — is the remaining window a strict palindrome after skipping the left or the right offender? The budget is now zero, so these inner checks allow no further mismatch.
4. Do the inner checks with **index bounds**, not slices: `s[i+1:j+1] == s[i+1:j+1][::-1]` is also O(n) but copies the string twice per branch; the index version touches each character at most a constant number of times and keeps space O(1).
5. Total work: the outer scan plus at most two disjoint-in-spirit inner scans over the unverified window → O(n).

## 5. Annotated Python solution

```python
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def is_pal(i: int, j: int) -> bool:      # strict check on s[i..j]
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True

        i, j = 0, len(s) - 1
        while i < j:
            if s[i] != s[j]:
                # budget forces the deletion to be s[i] or s[j] -- try both
                return is_pal(i + 1, j) or is_pal(i, j - 1)
            i += 1
            j -= 1
        return True                              # already a palindrome
```

## 6. Complexity

- **Time O(n)** — "one outer scan, and at most two inner scans over the not-yet-verified middle."
- **Space O(1)** — "indices only; no slices, no copies."

## 7. Edge-case traps

- **Trying only one branch** — greedy "always skip the left char" fails on strings like `"cbbcc"` (must skip right) or `"aabcba"` (must skip left); the `or` of both branches is mandatory.
- **Allowing a second deletion inside the branch** — the inner check must be *strict*; recursing into the tolerant version quietly permits two deletions and accepts strings like `"abcdba"` for the wrong reason (it happens to be a true one-deletion case — but `"cddcbb"`-style inputs expose the bug).
- **Already-palindromic input** — return `True` without consuming the budget; don't force a deletion.
- **Length 1 and 2** — any such string qualifies (`"ab"` → delete either char); the loop bounds must fall through to `True`.
- **Slicing in the hot path** — correctness survives, but on 10⁵-length near-palindromes the copies can be the difference between passing and TLE in slower runtimes.

## 8. Reusable template

Not DP. The template is **two-pointer scan + constant-size repair branch under an edit budget**; with the budget generalized to `k` it becomes the recursive/DP problem Valid Palindrome III, and the same "first mismatch pins the edit" logic drives one-swap and one-substitution variants.

## 9. Interviewer follow-up

- *"At most `k` deletions?"* — Valid Palindrome III (1216): the two-branch trick recursed naively is O(2^k); memoize on `(i, j)` and it becomes interval DP, equivalent to checking `len(s) - longest_palindromic_subsequence(s) <= k`.
- *"Ignore case and non-alphanumerics too?"* — compose with the filtering scan of Valid Palindrome (125), this problem's warmup: filter with pointer skips, then apply the same branch logic.
- *"Return the index to delete, not just yes/no"* — the scan already knows: it's `i` or `j` depending on which branch succeeded (or `-1`/any for an existing palindrome); a two-line change if your branches are explicit.
