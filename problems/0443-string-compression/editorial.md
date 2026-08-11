# String Compression — Editorial

## 1. Pattern recognition

Run-length encoding with an **in-place, O(1) extra space** demand: the combination of "scan runs" and "rewrite the same buffer" is the classic **read/write two-pointer** pattern — one cursor consumes the input, another produces output *behind it*. The parsing half is a miniature tokenizer (a token = one maximal run); the pointer half is the same compaction skeleton as Remove Duplicates and Move Zeroes. What makes it interview-worthy is the safety argument: you must be able to say *why* writing never clobbers unread data.

## 2. Brute force first

Build the compressed sequence in a fresh list, then copy it back into `chars` and return its length. Logically identical, O(n) time — and it silently uses O(n) extra space, which is the one thing the statement forbids. Interviewers use this problem to see whether you notice that the output for each run (1 character + at most 4 digits here) never exceeds the run's own length, which is exactly the invariant that makes in-place emission safe: `write` can never pass `read` **provided you finish reading a run before emitting it**. State that invariant out loud; it's the whole proof.

## 3. The key insight

**Consume an entire run with the read pointer first, then emit `char + digits(count)` at the write pointer — the emitted piece is never longer than the run it replaces, so the write cursor can never overrun unread input.**

## 4. Step-by-step derivation

1. Tokenize by runs: remember `ch = chars[read]`, advance `read` while it still sees `ch`. Now `count = read - start` and `read` already sits on the next run — no lookahead juggling, no `i+1 < n` peeking inside the emit logic.
2. Emit: write `ch`, then, *only if* `count > 1`, the digits of `count` in order. The "no digit for singles" rule is a spec quirk you encode once, in one `if` — enumerate the emission cases (1, 2–9, ≥10) before coding and the `str(count)` loop covers the last two uniformly.
3. Multi-digit counts: `str(count)` yields `'1','2'` for 12 — each digit is its own array slot. Writing the string `"12"` into a single slot is the canonical WA here.
4. Safety: for a run of length L the emission is `1 + len(str(L))` slots, and `1 + len(str(L)) <= L` for every `L >= 2` (for L = 1 we emit exactly 1). Since we emit only after `read` has moved past the run, `write <= read` always holds.
5. Return `write`. Whatever remains beyond it is garbage by contract — resist the urge to clean it.

## 5. Annotated Python solution

```python
class Solution:
    def compress(self, chars: list[str]) -> int:
        write = 0
        read = 0
        n = len(chars)
        while read < n:
            ch = chars[read]
            start = read
            while read < n and chars[read] == ch:   # measure the whole run first
                read += 1
            chars[write] = ch
            write += 1
            count = read - start
            if count > 1:                            # a lone char gets NO count digit
                for d in str(count):                 # 12 -> '1','2' (multi-char counts)
                    chars[write] = d
                    write += 1
        return write
```

## 6. Complexity

- **Time O(n)** — "each element is read once by the run scan and written at most once."
- **Space O(1)** — "two indices and a few-character digit string; no auxiliary buffer proportional to n."

## 7. Edge-case traps

- **Runs of length 1** (`["a","b","c"]`) — must emit no digit; the answer is the input unchanged.
- **A run of exactly 10** (`["o"]*10` → `'o','1','0'`) — the first multi-digit boundary; single-digit assumptions break here.
- **Count digits written as one string** instead of separate slots — `["b","12"]` is wrong shape, `["b","1","2"]` is right.
- **Alternating characters** (`["a","A","a","A"]` — case-sensitive!) — output length equals input length; `write` finishing equal to `read` is legal.
- **Trailing run at the very end** — the measure-first loop structure flushes it naturally; emit-as-you-go versions typically forget it.
- **Digits as input characters** (`["1","1","1"]` → `'1','3'`) — data and count digits look alike; only positions distinguish them, which is fine.

## 8. (DP section — not applicable)

Not DP. This trains the **read-runs / write-compacted two-pointer** template — the same consume-then-emit discipline behind Remove Duplicates from Sorted Array II and every in-place buffer rewrite.

## 9. Interviewer follow-up

- *"Decompress it"* — the inverse parse (`char, digits*`) can't be done in place left-to-right since output outgrows input; either compute the final length and fill **backwards**, or note the asymmetry — a sharp observation interviewers reward.
- *"Chunked/streaming input"* — a run can span chunk boundaries: carry `(current_char, count)` as state between chunks and merge; the run tokenizer generalizes cleanly.
- *"Why is the compressed form never longer?"* — prove `1 + len(str(L)) <= L` for `L >= 2` and equality of length 1 emissions; being able to produce this two-line proof on demand is the difference between using and understanding the invariant.
- *"Return the string instead, unlimited space"* — trivial with a list-join; the in-place constraint is the entire problem, so say what changes: nothing but the emission target.
