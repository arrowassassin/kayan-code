# Valid Palindrome — Editorial

## 1. Pattern recognition

"Same forwards and backwards" is the signature of the **two-pointer mirror scan**. What makes this a *parsing* exercise rather than a one-liner is the filter layered on top: some characters participate, others don't. Read the spec out loud and enumerate the token classes before typing — here there are exactly three: letters (compare case-insensitively), digits (compare as-is), everything else (invisible). Interviewers use this problem to watch whether you nail that classification cleanly or fumble it mid-loop.

## 2. Brute force first

`cleaned = [c.lower() for c in s if c.isalnum()]` then `cleaned == cleaned[::-1]`. That's O(n) time and O(n) space, completely correct, and in Python it's the honest pragmatic answer — say it in one breath. The reason to then write the two-pointer version isn't speed, it's **space**: O(1) extra, and it's the required warmup for the follow-up (Valid Palindrome II), where you must *resume* a scan mid-string — something the build-and-reverse trick cannot do.

## 3. The key insight

**Compare the string in place with two pointers, treating non-alphanumeric characters as if they didn't exist by stepping over them on the fly.**

## 4. Step-by-step derivation

1. A palindrome check needs each character matched with its mirror — pointers `i` from the left, `j` from the right.
2. The filter says punctuation has no mirror partner: before every comparison, advance `i` past non-alphanumerics and retreat `j` the same way.
3. Both skip loops must be guarded by `i < j`, not just the outer loop — otherwise a string like `".,;!"` runs a pointer off the end. Keeping the guard inside the skips means an all-punctuation (or empty) string falls through to `True` with zero special cases.
4. Compare with `.lower()` on both sides. `lower()` is a no-op on digits, so one normalization handles both classes — but the *comparison* itself must not be "is alnum then equal ignoring type": `'0' != 'P'` is precisely the trap test.
5. Match → move both pointers inward; mismatch → return `False` immediately.

## 5. Annotated Python solution

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1
        while i < j:
            # walk each pointer onto the next character that counts
            while i < j and not s[i].isalnum():
                i += 1
            while i < j and not s[j].isalnum():
                j -= 1
            if s[i].lower() != s[j].lower():
                return False
            i += 1
            j -= 1
        return True
```

## 6. Complexity

- **Time O(n)** — "every step moves a pointer inward, and the pointers cross after at most n moves total."
- **Space O(1)** — "no cleaned copy; two indices only."

## 7. Edge-case traps

- **`"0P"`** — the classic: digit vs letter must compare unequal; sloppy custom "normalize" arithmetic (e.g. `ord` masking) gets this wrong.
- **Empty string and all-punctuation strings** (`""`, `" "`, `".,"`) → `True`; these crash solutions whose skip loops lack the `i < j` guard.
- **Punctuation adjacent to the middle** (`"a."`, `"ab_a"`) — the pointers must be allowed to meet *on* a skipped character.
- **Mixed case across the mirror** (`"Able was I ere I saw Elba"`).
- **Underscore** is not alphanumeric — `str.isalnum()` handles it, but hand-rolled `c.isalpha() or c.isdigit()` rewrites sometimes drift into regex `\w`, which wrongly keeps `_` — yet `"0_0"` is still a palindrome either way; `"a_b"` variants separate the behaviors.

## 8. (DP section — not applicable)

Not DP. This trains the **filtered two-pointer mirror scan** — the base template that Valid Palindrome II extends with a one-deletion branch.

## 9. Interviewer follow-up

- *"Now you may delete at most one character"* — that is Valid Palindrome II (680), this problem's linked follow-up: on the first mismatch, branch into two plain scans (`skip i` or `skip j`) and accept if either finishes. Your in-place scan converts directly; the build-and-reverse version doesn't.
- *"Unicode input?"* — discuss what "alphanumeric" and "lowercase" mean outside ASCII (`str.casefold()`, combining characters, normalization) — the point is recognizing that the token-class definition is the spec, not the loop.
- *"Streaming, can't index from the right?"* — you'd need O(n) buffering; a hash-forward/hash-backward comparison is a good talking point.
