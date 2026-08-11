## Hint 1

Trying every possible deletion and re-checking is O(n²). Run the ordinary two-pointer palindrome check first — what is special about the *first* position where it fails?

## Hint 2

At the first mismatch `s[i] != s[j]`, every character outside `[i, j]` is already verified matched. If one deletion can fix the string, the deleted character must therefore be `s[i]` or `s[j]` — no other deletion changes anything inside the window that's still in doubt.

## Hint 3

So: scan until the first mismatch; then answer `is_palindrome(i+1, j) or is_palindrome(i, j-1)` using index ranges (no slicing — slices copy and can double your work). If the scan finishes with no mismatch, return `True` immediately.
