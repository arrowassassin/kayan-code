## Hint 1

This is three small jobs chained: extract words (letters only — punctuation is a separator, even mid-token like `"x!x"`), normalize them (lowercase), then count and pick the max among non-banned ones. Keep the jobs separate and each is trivial.

## Hint 2

Extraction is the only tricky part. Either scan character by character — accumulate letters, and flush the buffered word whenever you hit a non-letter — or, pragmatically in Python, `re.findall(r"[a-z]+", paragraph.lower())`. Turn `banned` into a `set` before counting.

## Hint 3

If you hand-roll the scan, the classic bug is losing the **final word** when the paragraph ends without punctuation. Either flush once more after the loop, or iterate over `paragraph + "."` so the sentinel forces the last flush. Track the running best while counting and you never need a second pass.
